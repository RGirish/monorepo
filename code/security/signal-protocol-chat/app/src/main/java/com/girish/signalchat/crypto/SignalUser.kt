package com.girish.signalchat.crypto

import org.signal.libsignal.protocol.ecc.ECKeyPair
import org.signal.libsignal.protocol.kem.KEMKeyPair
import org.signal.libsignal.protocol.kem.KEMKeyType
import org.signal.libsignal.protocol.state.KyberPreKeyRecord
import org.signal.libsignal.protocol.state.PreKeyBundle
import org.signal.libsignal.protocol.state.PreKeyRecord
import org.signal.libsignal.protocol.state.SignedPreKeyRecord

/**
 * One side of the conversation. [store] is this user's on-device trust store
 * -- identity, sessions, and pre-key material -- backed by files that survive
 * app restarts (see PersistentSignalProtocolStore). [preKeyBundle] is the
 * public counterpart: the equivalent of what a server would hand out to
 * anyone who wants to start a session with this user.
 *
 * Key material (pre-key/signed pre-key/Kyber pre-key, all id 1) is generated
 * once, the first time this runs against a fresh store, and reused on every
 * later launch -- regenerating it every launch would silently orphan
 * whatever bundle was already published to Firebase.
 */
class SignalUser(val name: String, val store: PersistentSignalProtocolStore) {

    private val deviceId = 1

    val preKeyBundle: PreKeyBundle =
        if (store.containsPreKey(PRE_KEY_ID)) loadExistingBundle() else generateAndStoreBundle()

    private fun loadExistingBundle(): PreKeyBundle {
        val preKey = store.loadPreKey(PRE_KEY_ID)
        val signedPreKey = store.loadSignedPreKey(SIGNED_PRE_KEY_ID)
        val kyberPreKey = store.loadKyberPreKey(KYBER_PRE_KEY_ID)
        return PreKeyBundle(
            store.localRegistrationId,
            deviceId,
            PRE_KEY_ID,
            preKey.keyPair.publicKey,
            SIGNED_PRE_KEY_ID,
            signedPreKey.keyPair.publicKey,
            signedPreKey.signature,
            store.identityKeyPair.publicKey,
            KYBER_PRE_KEY_ID,
            kyberPreKey.keyPair.publicKey,
            kyberPreKey.signature,
        )
    }

    private fun generateAndStoreBundle(): PreKeyBundle {
        val identityKeyPair = store.identityKeyPair

        val preKeyPair = ECKeyPair.generate()
        store.storePreKey(PRE_KEY_ID, PreKeyRecord(PRE_KEY_ID, preKeyPair))

        // Signed by the long-term identity key so a recipient can verify it
        // really came from this identity (not a man-in-the-middle
        // substituting their own key on the server).
        val signedPreKeyPair = ECKeyPair.generate()
        val signedPreKeySignature =
            identityKeyPair.privateKey.calculateSignature(signedPreKeyPair.publicKey.serialize())
        store.storeSignedPreKey(
            SIGNED_PRE_KEY_ID,
            SignedPreKeyRecord(SIGNED_PRE_KEY_ID, System.currentTimeMillis(), signedPreKeyPair, signedPreKeySignature)
        )

        // The Kyber (post-quantum) pre-key, signed the same way. PQXDH mixes
        // this in alongside the classic EC agreement.
        val kyberKeyPair = KEMKeyPair.generate(KEMKeyType.KYBER_1024)
        val kyberPreKeySignature =
            identityKeyPair.privateKey.calculateSignature(kyberKeyPair.publicKey.serialize())
        store.storeKyberPreKey(
            KYBER_PRE_KEY_ID,
            KyberPreKeyRecord(KYBER_PRE_KEY_ID, System.currentTimeMillis(), kyberKeyPair, kyberPreKeySignature)
        )

        return PreKeyBundle(
            store.localRegistrationId,
            deviceId,
            PRE_KEY_ID,
            preKeyPair.publicKey,
            SIGNED_PRE_KEY_ID,
            signedPreKeyPair.publicKey,
            signedPreKeySignature,
            identityKeyPair.publicKey,
            KYBER_PRE_KEY_ID,
            kyberKeyPair.publicKey,
            kyberPreKeySignature,
        )
    }

    private companion object {
        const val PRE_KEY_ID = 1
        const val SIGNED_PRE_KEY_ID = 1
        const val KYBER_PRE_KEY_ID = 1
    }
}
