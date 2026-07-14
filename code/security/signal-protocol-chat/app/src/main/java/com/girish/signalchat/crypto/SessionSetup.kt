package com.girish.signalchat.crypto

import org.signal.libsignal.protocol.SessionBuilder
import org.signal.libsignal.protocol.UsePqRatchet

/**
 * Runs X3DH/PQXDH: [initiator] fetches [recipient]'s published pre-key bundle
 * (simulating a server lookup) and derives the initial root key for messages
 * sent from initiator to recipient, storing it in initiator's own session store.
 *
 * This only touches initiator's side. Recipient's side of the session isn't
 * created yet -- that happens implicitly the moment recipient decrypts the
 * first message (Stage 4), by reading the pre-key IDs embedded in it.
 */
fun establishOutgoingSession(initiator: SignalUser, recipient: SignalUser) {
    SessionBuilder(initiator.store, recipient.address)
        .process(recipient.preKeyBundle, UsePqRatchet.YES)
}

fun SignalUser.hasSessionWith(other: SignalUser): Boolean =
    store.containsSession(other.address)
