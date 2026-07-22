package com.girish.signalchat.crypto

import org.signal.libsignal.protocol.SessionCipher
import org.signal.libsignal.protocol.SignalProtocolAddress
import org.signal.libsignal.protocol.UsePqRatchet
import org.signal.libsignal.protocol.message.CiphertextMessage
import org.signal.libsignal.protocol.message.PreKeySignalMessage
import org.signal.libsignal.protocol.message.SignalMessage
import java.nio.charset.StandardCharsets

/** What actually crosses "the wire" -- opaque ciphertext plus the type tag needed to parse it. */
data class EncryptedEnvelope(val type: Int, val bytes: ByteArray)

/**
 * The first envelope in a conversation is a PreKeySignalMessage (type == PREKEY_TYPE):
 * it carries the sender's identity/base key and which of the recipient's pre-keys were
 * used, so the recipient can build their side of the session on receipt. Every later
 * envelope is a plain SignalMessage (type == WHISPER_TYPE) -- just ratchet-encrypted
 * ciphertext, since both sides already share session state by then.
 */
fun SignalUser.encryptFor(recipientAddress: SignalProtocolAddress, plaintext: String): EncryptedEnvelope {
    val cipher = SessionCipher(store, recipientAddress)
    val message = cipher.encrypt(plaintext.toByteArray(StandardCharsets.UTF_8))
    return EncryptedEnvelope(message.type, message.serialize())
}

/** Decrypting a PreKeySignalMessage implicitly builds this user's side of the session. */
fun SignalUser.decryptFrom(senderAddress: SignalProtocolAddress, envelope: EncryptedEnvelope): String {
    val cipher = SessionCipher(store, senderAddress)
    val plaintextBytes = when (envelope.type) {
        CiphertextMessage.PREKEY_TYPE ->
            cipher.decrypt(PreKeySignalMessage(envelope.bytes), UsePqRatchet.YES)
        CiphertextMessage.WHISPER_TYPE ->
            cipher.decrypt(SignalMessage(envelope.bytes))
        else -> error("Unrecognized Signal ciphertext type: ${envelope.type}")
    }
    return String(plaintextBytes, StandardCharsets.UTF_8)
}
