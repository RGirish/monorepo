package com.girish.signalchat.crypto

import org.signal.libsignal.protocol.SessionBuilder
import org.signal.libsignal.protocol.SignalProtocolAddress
import org.signal.libsignal.protocol.UsePqRatchet
import org.signal.libsignal.protocol.state.PreKeyBundle

/**
 * Runs X3DH/PQXDH: [initiator] processes [remoteBundle] (fetched from wherever
 * the recipient published it -- Firestore) and derives the initial root key
 * for messages sent from initiator to [remoteAddress], storing it in
 * initiator's own session store.
 *
 * This only touches initiator's side. The remote side of the session isn't
 * created yet -- that happens implicitly the moment they decrypt the first
 * message, by reading the pre-key IDs embedded in it.
 */
fun establishOutgoingSession(initiator: SignalUser, remoteAddress: SignalProtocolAddress, remoteBundle: PreKeyBundle) {
    SessionBuilder(initiator.store, remoteAddress)
        .process(remoteBundle, UsePqRatchet.YES)
}

fun SignalUser.hasSessionWith(address: SignalProtocolAddress): Boolean =
    store.containsSession(address)
