package com.girish.signalchat

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.safeDrawingPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Button
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.girish.signalchat.crypto.EncryptedEnvelope
import com.girish.signalchat.crypto.SignalUser
import com.girish.signalchat.crypto.decryptFrom
import com.girish.signalchat.crypto.encryptFor
import com.girish.signalchat.crypto.establishOutgoingSession
import com.girish.signalchat.crypto.hasSessionWith

data class ChatMessage(val sender: String, val text: String)

// A packet as it would appear to an eavesdropper on the wire: sender/recipient
// name plus opaque ciphertext -- never plaintext.
data class NetworkPacket(val from: String, val to: String, val envelope: EncryptedEnvelope)

// Short hex prefix of the identity public key, just so two runs visibly produce
// two different identities -- not a real safety-number fingerprint.
fun SignalUser.shortFingerprint(): String =
    store.identityKeyPair.publicKey.fingerprint.take(12)

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                Surface(modifier = Modifier.fillMaxSize().safeDrawingPadding()) {
                    TwoUserChatShell()
                }
            }
        }
    }
}

@Composable
fun TwoUserChatShell() {
    val alice = remember { SignalUser("Alice") }
    val bob = remember { SignalUser("Bob") }

    // Alice initiates: she fetches Bob's pre-key bundle and runs X3DH/PQXDH,
    // giving her an outgoing session. Bob has no session yet -- his side is
    // only created once he decrypts Alice's first message.
    remember(alice, bob) {
        establishOutgoingSession(alice, bob)
        Unit
    }

    // The only state shared between the two panes -- the "wire." Each pane
    // only ever reads ciphertext out of it and decrypts locally with its own
    // session state; it never touches the other pane's keys or plaintext.
    val network = remember { mutableStateListOf<NetworkPacket>() }

    Row(modifier = Modifier.fillMaxSize()) {
        UserPane(
            user = alice,
            other = bob,
            modifier = Modifier.weight(1f),
            network = network,
            onSend = { text -> network.add(NetworkPacket(alice.name, bob.name, alice.encryptFor(bob, text))) }
        )
        HorizontalDivider(modifier = Modifier.fillMaxHeight().width(1.dp))
        UserPane(
            user = bob,
            other = alice,
            modifier = Modifier.weight(1f),
            network = network,
            onSend = { text -> network.add(NetworkPacket(bob.name, alice.name, bob.encryptFor(alice, text))) }
        )
    }
}

@Composable
fun UserPane(
    user: SignalUser,
    other: SignalUser,
    modifier: Modifier = Modifier,
    network: List<NetworkPacket>,
    onSend: (String) -> Unit
) {
    var input by remember { mutableStateOf("") }
    val displayed = remember { mutableStateListOf<ChatMessage>() }
    var processedCount by remember { mutableStateOf(0) }

    // Bob can't send until he's decrypted a first message from Alice -- only
    // the initiator runs X3DH up front; the responder's session is built as a
    // side effect of decrypting that first PreKeySignalMessage. This has to be
    // real Compose state (not a plain re-evaluated call into the libsignal
    // store) -- otherwise nothing tells this composable to recompose at the
    // exact moment decryption below actually creates the session.
    var canSend by remember { mutableStateOf(user.hasSessionWith(other)) }

    // Decrypt each new packet addressed to this user exactly once -- the Double
    // Ratchet deletes a message key immediately after use, so decrypting the
    // same envelope twice would throw DuplicateMessageException.
    LaunchedEffect(network.size) {
        for (i in processedCount until network.size) {
            val packet = network[i]
            if (packet.to == user.name) {
                displayed.add(ChatMessage(packet.from, user.decryptFrom(other, packet.envelope)))
            }
        }
        processedCount = network.size
        canSend = user.hasSessionWith(other)
    }

    Column(modifier = modifier.padding(8.dp)) {
        Text(text = user.name, style = MaterialTheme.typography.titleMedium)
        Text(
            text = "identity ${user.shortFingerprint()}",
            style = MaterialTheme.typography.labelSmall
        )
        Text(
            text = if (canSend) "session → ${other.name}: established" else "session → ${other.name}: none yet",
            style = MaterialTheme.typography.labelSmall
        )
        Spacer(modifier = Modifier.height(8.dp))
        LazyColumn(modifier = Modifier.weight(1f)) {
            items(displayed) { msg ->
                Text("${msg.sender}: ${msg.text}")
            }
        }
        if (!canSend) {
            Text(
                text = "waiting for a first message to establish a session",
                style = MaterialTheme.typography.labelSmall
            )
        }
        Row {
            OutlinedTextField(
                value = input,
                onValueChange = { input = it },
                modifier = Modifier.weight(1f),
                label = { Text("Message") },
                enabled = canSend
            )
            Button(
                onClick = {
                    if (input.isNotBlank()) {
                        displayed.add(ChatMessage(user.name, input))
                        onSend(input)
                        input = ""
                    }
                },
                enabled = canSend
            ) {
                Text("Send")
            }
        }
    }
}
