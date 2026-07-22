package com.girish.signalchat

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.safeDrawingPadding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import com.girish.signalchat.backend.ensureSignedIn
import com.girish.signalchat.backend.fetchPreKeyBundle
import com.girish.signalchat.backend.listenForMessages
import com.girish.signalchat.backend.otherUid
import com.girish.signalchat.backend.publishPreKeyBundle
import com.girish.signalchat.backend.sendEnvelope
import com.girish.signalchat.crypto.EncryptedEnvelope
import com.girish.signalchat.crypto.PersistentSignalProtocolStore
import com.girish.signalchat.crypto.SignalUser
import com.girish.signalchat.crypto.decryptFrom
import com.girish.signalchat.crypto.encryptFor
import com.girish.signalchat.crypto.establishOutgoingSession
import com.girish.signalchat.crypto.hasSessionWith
import java.io.File
import kotlinx.coroutines.launch
import org.signal.libsignal.protocol.SignalProtocolAddress

data class ChatMessage(val sender: String, val text: String)

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                Surface(modifier = Modifier.fillMaxSize().safeDrawingPadding()) {
                    ChatScreen()
                }
            }
        }
    }
}

/**
 * The real 2-person chat. Signs in, publishes this device's pre-key bundle,
 * and either establishes an outgoing session (if this device gets there
 * first) or waits to become the responder by decrypting the other side's
 * first message -- whichever happens first is fine, since which side ends
 * up initiating is genuinely unpredictable once both are talking over a
 * real, asynchronous network instead of the local in-memory demo.
 */
@Composable
fun ChatScreen() {
    val context = LocalContext.current
    val coroutineScope = rememberCoroutineScope()

    var myUid by remember { mutableStateOf<String?>(null) }
    var otherUidState by remember { mutableStateOf<String?>(null) }
    var me by remember { mutableStateOf<SignalUser?>(null) }
    var otherAddress by remember { mutableStateOf<SignalProtocolAddress?>(null) }
    var status by remember { mutableStateOf("signing in...") }
    var canSend by remember { mutableStateOf(false) }
    val messages = remember { mutableStateListOf<ChatMessage>() }
    var input by remember { mutableStateOf("") }

    LaunchedEffect(Unit) {
        val uid = ensureSignedIn()
        val other = otherUid(uid)
        val user = SignalUser(uid, PersistentSignalProtocolStore(File(context.filesDir, "real-signal-store")))
        val address = SignalProtocolAddress(other, 1)

        myUid = uid
        otherUidState = other
        me = user
        otherAddress = address

        publishPreKeyBundle(uid, user.preKeyBundle)

        if (user.hasSessionWith(address)) {
            canSend = true
            status = "connected"
        } else {
            status = "establishing session..."
            try {
                establishOutgoingSession(user, address, fetchPreKeyBundle(other))
                canSend = true
                status = "connected"
            } catch (e: Exception) {
                status = "waiting for ${other.take(8)}... to come online"
            }
        }
    }

    // Listen for incoming messages regardless of whether our own outgoing
    // session is established yet -- decrypting someone else's first message
    // is exactly how the *responder* side of a session gets built.
    DisposableEffect(myUid) {
        val uid = myUid ?: return@DisposableEffect onDispose {}
        val registration = listenForMessages(uid) { incoming, delete ->
            coroutineScope.launch {
                val user = me ?: return@launch
                val address = otherAddress ?: return@launch
                try {
                    val plaintext = user.decryptFrom(address, EncryptedEnvelope(incoming.type, incoming.ciphertext))
                    messages.add(ChatMessage(incoming.from, plaintext))
                    delete()
                    if (!canSend) {
                        canSend = true
                        status = "connected"
                    }
                } catch (e: Exception) {
                    // Already-delivered or replayed envelope -- nothing to recover, just drop it.
                }
            }
        }
        onDispose { registration.remove() }
    }

    Column(modifier = Modifier.fillMaxSize().padding(8.dp)) {
        Text(text = "You: ${myUid?.take(8) ?: "..."}", style = MaterialTheme.typography.labelSmall)
        Text(text = "Chatting with: ${otherUidState?.take(8) ?: "..."}", style = MaterialTheme.typography.labelSmall)
        Text(text = status, style = MaterialTheme.typography.labelSmall)
        Spacer(modifier = Modifier.height(8.dp))
        LazyColumn(modifier = Modifier.weight(1f)) {
            items(messages) { msg ->
                Text("${msg.sender.take(8)}: ${msg.text}")
            }
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
                    val user = me
                    val address = otherAddress
                    val uid = myUid
                    val other = otherUidState
                    if (input.isNotBlank() && user != null && address != null && uid != null && other != null) {
                        val text = input
                        input = ""
                        val envelope = user.encryptFor(address, text)
                        messages.add(ChatMessage(uid, text))
                        coroutineScope.launch {
                            sendEnvelope(other, uid, envelope.type, envelope.bytes)
                        }
                    }
                },
                enabled = canSend
            ) {
                Text("Send")
            }
        }
    }
}
