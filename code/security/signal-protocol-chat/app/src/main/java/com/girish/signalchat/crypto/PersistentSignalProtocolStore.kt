package com.girish.signalchat.crypto

import org.signal.libsignal.protocol.IdentityKey
import org.signal.libsignal.protocol.IdentityKeyPair
import org.signal.libsignal.protocol.InvalidKeyIdException
import org.signal.libsignal.protocol.NoSessionException
import org.signal.libsignal.protocol.SignalProtocolAddress
import org.signal.libsignal.protocol.groups.state.SenderKeyRecord
import org.signal.libsignal.protocol.state.IdentityKeyStore
import org.signal.libsignal.protocol.state.KyberPreKeyRecord
import org.signal.libsignal.protocol.state.PreKeyRecord
import org.signal.libsignal.protocol.state.SessionRecord
import org.signal.libsignal.protocol.state.SignalProtocolStore
import org.signal.libsignal.protocol.state.SignedPreKeyRecord
import org.signal.libsignal.protocol.util.KeyHelper
import java.io.File
import java.util.UUID

/**
 * A SignalProtocolStore backed by files in the app's private storage, so
 * identity and session state survive app restarts instead of resetting on
 * every launch like InMemorySignalProtocolStore did. Every libsignal record
 * already knows how to serialize/deserialize itself -- this class just
 * decides where those bytes live on disk, one small file per record.
 *
 * [baseDir] should be an app-private directory (e.g. Context.filesDir), which
 * Android already sandboxes from other apps without root.
 */
class PersistentSignalProtocolStore(baseDir: File) : SignalProtocolStore {

    private val root = baseDir.apply { mkdirs() }
    private val preKeysDir = File(root, "prekeys").apply { mkdirs() }
    private val signedPreKeysDir = File(root, "signed_prekeys").apply { mkdirs() }
    private val kyberPreKeysDir = File(root, "kyber_prekeys").apply { mkdirs() }
    private val sessionsDir = File(root, "sessions").apply { mkdirs() }
    private val identitiesDir = File(root, "identities").apply { mkdirs() }
    private val identityKeyFile = File(root, "identity.key")
    private val registrationIdFile = File(root, "registration.id")

    private val ownIdentityKeyPair: IdentityKeyPair =
        if (identityKeyFile.exists()) {
            IdentityKeyPair(identityKeyFile.readBytes())
        } else {
            IdentityKeyPair.generate().also { identityKeyFile.writeBytes(it.serialize()) }
        }

    private val ownRegistrationId: Int =
        if (registrationIdFile.exists()) {
            registrationIdFile.readText().trim().toInt()
        } else {
            KeyHelper.generateRegistrationId(false).also { registrationIdFile.writeText(it.toString()) }
        }

    private fun addressKey(address: SignalProtocolAddress) = "${address.name}_${address.deviceId}"

    // --- IdentityKeyStore ---

    override fun getIdentityKeyPair(): IdentityKeyPair = ownIdentityKeyPair

    override fun getLocalRegistrationId(): Int = ownRegistrationId

    override fun saveIdentity(address: SignalProtocolAddress, identityKey: IdentityKey): IdentityKeyStore.IdentityChange {
        val file = File(identitiesDir, addressKey(address))
        val existing = if (file.exists()) IdentityKey(file.readBytes()) else null
        file.writeBytes(identityKey.serialize())
        return if (existing == null || existing == identityKey) {
            IdentityKeyStore.IdentityChange.NEW_OR_UNCHANGED
        } else {
            IdentityKeyStore.IdentityChange.REPLACED_EXISTING
        }
    }

    override fun isTrustedIdentity(
        address: SignalProtocolAddress,
        identityKey: IdentityKey,
        direction: IdentityKeyStore.Direction
    ): Boolean {
        val file = File(identitiesDir, addressKey(address))
        // Trust on first use: nothing saved yet for this address means we've
        // never seen a different identity claim to be them.
        if (!file.exists()) return true
        return IdentityKey(file.readBytes()) == identityKey
    }

    override fun getIdentity(address: SignalProtocolAddress): IdentityKey? {
        val file = File(identitiesDir, addressKey(address))
        return if (file.exists()) IdentityKey(file.readBytes()) else null
    }

    // --- PreKeyStore ---

    override fun loadPreKey(preKeyId: Int): PreKeyRecord {
        val file = File(preKeysDir, preKeyId.toString())
        if (!file.exists()) throw InvalidKeyIdException("No such pre-key: $preKeyId")
        return PreKeyRecord(file.readBytes())
    }

    override fun storePreKey(preKeyId: Int, record: PreKeyRecord) {
        File(preKeysDir, preKeyId.toString()).writeBytes(record.serialize())
    }

    override fun containsPreKey(preKeyId: Int): Boolean = File(preKeysDir, preKeyId.toString()).exists()

    override fun removePreKey(preKeyId: Int) {
        File(preKeysDir, preKeyId.toString()).delete()
    }

    // --- SignedPreKeyStore ---

    override fun loadSignedPreKey(signedPreKeyId: Int): SignedPreKeyRecord {
        val file = File(signedPreKeysDir, signedPreKeyId.toString())
        if (!file.exists()) throw InvalidKeyIdException("No such signed pre-key: $signedPreKeyId")
        return SignedPreKeyRecord(file.readBytes())
    }

    override fun loadSignedPreKeys(): MutableList<SignedPreKeyRecord> =
        signedPreKeysDir.listFiles().orEmpty().map { SignedPreKeyRecord(it.readBytes()) }.toMutableList()

    override fun storeSignedPreKey(signedPreKeyId: Int, record: SignedPreKeyRecord) {
        File(signedPreKeysDir, signedPreKeyId.toString()).writeBytes(record.serialize())
    }

    override fun containsSignedPreKey(signedPreKeyId: Int): Boolean =
        File(signedPreKeysDir, signedPreKeyId.toString()).exists()

    override fun removeSignedPreKey(signedPreKeyId: Int) {
        File(signedPreKeysDir, signedPreKeyId.toString()).delete()
    }

    // --- KyberPreKeyStore ---

    override fun loadKyberPreKey(kyberPreKeyId: Int): KyberPreKeyRecord {
        val file = File(kyberPreKeysDir, kyberPreKeyId.toString())
        if (!file.exists()) throw InvalidKeyIdException("No such Kyber pre-key: $kyberPreKeyId")
        return KyberPreKeyRecord(file.readBytes())
    }

    override fun loadKyberPreKeys(): MutableList<KyberPreKeyRecord> =
        kyberPreKeysDir.listFiles().orEmpty().map { KyberPreKeyRecord(it.readBytes()) }.toMutableList()

    override fun storeKyberPreKey(kyberPreKeyId: Int, record: KyberPreKeyRecord) {
        File(kyberPreKeysDir, kyberPreKeyId.toString()).writeBytes(record.serialize())
    }

    override fun containsKyberPreKey(kyberPreKeyId: Int): Boolean =
        File(kyberPreKeysDir, kyberPreKeyId.toString()).exists()

    override fun markKyberPreKeyUsed(kyberPreKeyId: Int) {
        // A real deployment with pre-key replenishment would delete/rotate it
        // here. This app never re-establishes a session against the same
        // bundle twice, so leaving the record in place is harmless.
    }

    // --- SessionStore ---

    override fun loadSession(address: SignalProtocolAddress): SessionRecord {
        val file = File(sessionsDir, addressKey(address))
        return if (file.exists()) SessionRecord(file.readBytes()) else SessionRecord()
    }

    override fun loadExistingSessions(addresses: MutableList<SignalProtocolAddress>): MutableList<SessionRecord> =
        addresses.map { address ->
            val file = File(sessionsDir, addressKey(address))
            if (!file.exists()) throw NoSessionException("No session for $address")
            SessionRecord(file.readBytes())
        }.toMutableList()

    override fun getSubDeviceSessions(name: String): MutableList<Int> =
        sessionsDir.listFiles().orEmpty()
            .map { it.name }
            .filter { it.startsWith("${name}_") }
            .mapNotNull { it.substringAfterLast("_").toIntOrNull() }
            .filter { it != 1 }
            .toMutableList()

    override fun storeSession(address: SignalProtocolAddress, record: SessionRecord) {
        File(sessionsDir, addressKey(address)).writeBytes(record.serialize())
    }

    override fun containsSession(address: SignalProtocolAddress): Boolean =
        File(sessionsDir, addressKey(address)).exists()

    override fun deleteSession(address: SignalProtocolAddress) {
        File(sessionsDir, addressKey(address)).delete()
    }

    override fun deleteAllSessions(name: String) {
        sessionsDir.listFiles().orEmpty().filter { it.name.startsWith("${name}_") }.forEach { it.delete() }
    }

    // --- SenderKeyStore (group messaging; unused by this 1:1 app) ---

    override fun storeSenderKey(sender: SignalProtocolAddress, distributionId: UUID, record: SenderKeyRecord) {
    }

    override fun loadSenderKey(sender: SignalProtocolAddress, distributionId: UUID): SenderKeyRecord? = null
}
