package com.girish.signalchat.crypto

import org.signal.libsignal.protocol.IdentityKeyPair
import org.signal.libsignal.protocol.SignalProtocolAddress
import org.signal.libsignal.protocol.ecc.ECKeyPair
import org.signal.libsignal.protocol.kem.KEMKeyPair
import org.signal.libsignal.protocol.kem.KEMKeyType
import org.signal.libsignal.protocol.state.KyberPreKeyRecord
import org.signal.libsignal.protocol.state.PreKeyBundle
import org.signal.libsignal.protocol.state.PreKeyRecord
import org.signal.libsignal.protocol.state.SignedPreKeyRecord
import org.signal.libsignal.protocol.state.impl.InMemorySignalProtocolStore
import org.signal.libsignal.protocol.util.KeyHelper

/**
 * One side of the conversation. Everything a real Signal client would keep on-device:
 * a long-term identity, a registration id, and the private halves of the pre-keys it
 * has published. [preKeyBundle] is the public counterpart -- the equivalent of what
 * the *server* would hand out to anyone who wants to start a session with this user.
 */
class SignalUser(val name: String) {

    private val deviceId = 1
    val address = SignalProtocolAddress(name, deviceId)

    private val registrationId = KeyHelper.generateRegistrationId(false)
    private val identityKeyPair = IdentityKeyPair.generate()

    // Holds identity, session, one-time pre-key, signed pre-key, and Kyber
    // pre-key state -- this is the on-device "trust store" for this user.
    val store = InMemorySignalProtocolStore(identityKeyPair, registrationId)

    val preKeyBundle: PreKeyBundle

    init {
        val preKeyId = 1
        val preKeyPair = ECKeyPair.generate()
        store.storePreKey(preKeyId, PreKeyRecord(preKeyId, preKeyPair))

        // The signed pre-key is signed by the long-term identity key, so a
        // recipient can verify it really came from this identity (not a
        // man-in-the-middle substituting their own key on the server).
        val signedPreKeyId = 1
        val signedPreKeyPair = ECKeyPair.generate()
        val signedPreKeySignature =
            identityKeyPair.privateKey.calculateSignature(signedPreKeyPair.publicKey.serialize())
        store.storeSignedPreKey(
            signedPreKeyId,
            SignedPreKeyRecord(signedPreKeyId, System.currentTimeMillis(), signedPreKeyPair, signedPreKeySignature)
        )

        // The Kyber (post-quantum) pre-key, signed the same way. PQXDH mixes
        // this in alongside the classic EC agreement.
        val kyberPreKeyId = 1
        val kyberKeyPair = KEMKeyPair.generate(KEMKeyType.KYBER_1024)
        val kyberPreKeySignature =
            identityKeyPair.privateKey.calculateSignature(kyberKeyPair.publicKey.serialize())
        store.storeKyberPreKey(
            kyberPreKeyId,
            KyberPreKeyRecord(kyberPreKeyId, System.currentTimeMillis(), kyberKeyPair, kyberPreKeySignature)
        )

        preKeyBundle = PreKeyBundle(
            registrationId,
            deviceId,
            preKeyId,
            preKeyPair.publicKey,
            signedPreKeyId,
            signedPreKeyPair.publicKey,
            signedPreKeySignature,
            identityKeyPair.publicKey,
            kyberPreKeyId,
            kyberKeyPair.publicKey,
            kyberPreKeySignature,
        )
    }
}
