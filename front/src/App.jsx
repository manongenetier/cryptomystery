import React, { useState, useRef, useEffect } from "react";
import { cryptoApi } from "./services/cryptoApi";
import "./App.css";
import Typewriter from "./SplashScreen";

function MessageCard({ msg, side, onDecode, loading }) {
  const isSent = msg.from === side;
  return (
    <div
      className={`message-card ${isSent ? "sent" : msg.decoded ? "received" : "pending"}`}
    >
      <div className="message-header">
        <span>{isSent ? "Envoyé" : "Reçu"}</span>
        <span>{msg.time}</span>
      </div>
      <div className="message-content">
        <p>
          <code>{msg.displayText}</code>
        </p>
        {msg.decoded && <p>{msg.decoded}</p>}
      </div>
      {!isSent && !msg.decoded && (
        <button
          className="decode-btn"
          onClick={() => onDecode(msg)}
          disabled={loading}
        >
          Déchiffrer
        </button>
      )}
    </div>
  );
}

function PersonPanel({
  side,
  label,
  messages,
  paquetRef,
  onMessageSent,
  onDecode,
  initialized,
}) {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;
    if (!paquetRef.current) {
      setError("Le paquet n'est pas encore initialisé.");
      return;
    }
    try {
      setLoading(true);
      setError("");
      const response = await cryptoApi.coder(input.trim(), paquetRef.current);
      paquetRef.current = response.etat_paquet;
      onMessageSent({
        id: Date.now(),
        from: side,
        displayText: response.result.join(", "),
        coded: response.result,
        decoded: null,
        time: new Date().toLocaleTimeString("fr-FR", {
          hour: "2-digit",
          minute: "2-digit",
        }),
      });
      setInput("");
    } catch {
      setError("Erreur lors du chiffrage.");
    } finally {
      setLoading(false);
    }
  };

  const handleDecode = async (msg) => {
    if (!paquetRef.current) {
      setError("Le paquet n'est pas encore initialisé.");
      return;
    }
    try {
      setLoading(true);
      setError("");
      const response = await cryptoApi.decoder(msg.coded, paquetRef.current);
      paquetRef.current = response.etat_paquet;
      onDecode(msg.id, response.decode);
    } catch {
      setError("Erreur lors du déchiffrage.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="person-container">
      <div className="person-header">
        <h2>{label}</h2>
        <span className="info-badge">
          {paquetRef.current ? "● Paquet actif" : "En attente..."}
        </span>
      </div>

      <div className="person-content">

        {/* Affichage de l'état du paquet */}
        <div className="paquet-state-section">
          <div className="paquet-state-header">
            <h4>ÉTAT DE MON PAQUET</h4>
            <span>{paquetRef.current?.length || 0} cartes</span>
          </div>
          <div className="paquet-stats">
            <span>
              {paquetRef.current
                ?.slice(0, 5)
                .map((c) => c.carte.split("-")[0])
                .join(", ")}
              ...
            </span>
          </div>
          <details>
            <summary
              style={{
                fontSize: "0.7rem",
                color: "rgba(255,255,255,0.4)",
                cursor: "pointer",
              }}
            >
              Voir toutes les cartes
            </summary>
            <div className="paquet-state-preview">
              {paquetRef.current?.map((carte, idx) => (
                <span
                  key={idx}
                  className="paquet-card-mini"
                  title={`${carte.carte} = ${carte.valeur}`}
                >
                  {carte.carte}
                </span>
              ))}
            </div>
          </details>
        </div>

        {/* Zone de saisie */}
        <div className="message-input-section">
          <h3>✉ Écrire un message</h3>
          <textarea
            className="message-input"
            placeholder={
              initialized
                ? "Votre message secret..."
                : "Initialisez le paquet d'abord..."
            }
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) =>
              e.key === "Enter" &&
              !e.shiftKey &&
              !loading &&
              (e.preventDefault(), handleSend())
            }
            disabled={!paquetRef.current || loading}
          />
          {error && <p className="error-message">{error}</p>}
          <button
            className="send-btn"
            onClick={handleSend}
            disabled={!paquetRef.current || loading || !input.trim()}
          >
            {loading ? "En cours..." : "Chiffrer & Envoyer"}
          </button>
        </div>

        {/* Liste des messages */}
        <div className="messages-section">
          <h3>Messages</h3>
          <div className="messages-list">
            {messages.length === 0 ? (
              <p className="no-messages">Aucun message pour l'instant...</p>
            ) : (
              messages.map((msg) => (
                <MessageCard
                  key={msg.id}
                  msg={msg}
                  side={side}
                  onDecode={handleDecode}
                  loading={loading}
                />
              ))
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default function App() {
  const [splashDone, setSplashDone] = useState(false);
  const [messages, setMessages] = useState([]);
  const [initialized, setInitialized] = useState(false);
  const [initLoading, setInitLoading] = useState(false);
  const [initError, setInitError] = useState("");

  // Un seul /init → copie identique donnée aux deux agents
  // Chaque paquet évolue ensuite indépendamment mais en miroir
  const paquetA = useRef(null);
  const paquetB = useRef(null);

  const handleInit = async () => {
    try {
      setInitLoading(true);
      setInitError("");
      const paquet = await cryptoApi.init();
      // Copie profonde identique pour les deux agents
      paquetA.current = JSON.parse(JSON.stringify(paquet));
      paquetB.current = JSON.parse(JSON.stringify(paquet));
      setInitialized(true);
    } catch {
      setInitError("Erreur lors de l'initialisation.");
    } finally {
      setInitLoading(false);
    }
  };

  const handleMessageSent = (msg) => {
    setMessages((prev) => [...prev, msg]);
  };

  const handleDecode = (msgId, decodedText) => {
    setMessages((prev) =>
      prev.map((m) => (m.id === msgId ? { ...m, decoded: decodedText } : m)),
    );
  };

  return (
    <div className="app">
      {/* Splash */}
      <div id="intro" style={{ display: splashDone ? "none" : "flex" }}>
        <p>
          {!splashDone && (
            <Typewriter
              text="Bienvenue à Crypto Mystery"
              delay={100}
              onComplete={() => setSplashDone(true)}
            />
          )}
        </p>
      </div>

      {/* App principale */}
      {splashDone && (
        <>
          {/* Bouton d'init global centré en haut */}
          {!initialized && (
            <div style={{ textAlign: "center", padding: "16px 0 8px" }}>
              <button
                className="init-btn"
                onClick={handleInit}
                disabled={initLoading}
                style={{ fontSize: "1rem", padding: "12px 32px" }}
              >
                {initLoading
                  ? "Initialisation..."
                  : "Initialiser le paquet partagé"}
              </button>
              {initError && (
                <p
                  className="error-message"
                  style={{ display: "inline-block", marginLeft: 12 }}
                >
                  {initError}
                </p>
              )}
            </div>
          )}
          {initialized && (
            <div
              style={{
                textAlign: "center",
                padding: "10px 0 4px",
                fontSize: "0.9rem",
                color: "#a3e635",
                fontFamily: "'Pixelify Sans', sans-serif",
                letterSpacing: 1,
              }}
            >
              ✓ Paquet synchronisé — les deux agents sont prêts
            </div>
          )}

          <div className="chat-container">
            <PersonPanel
              side="A"
              label="Manon"
              messages={messages}
              paquetRef={paquetA}
              onMessageSent={handleMessageSent}
              onDecode={handleDecode}
              initialized={initialized}
            />
            <PersonPanel
              side="B"
              label="Bahdja"
              messages={messages}
              paquetRef={paquetB}
              onMessageSent={handleMessageSent}
              onDecode={handleDecode}
              initialized={initialized}
            />
          </div>
        </>
      )}
    </div>
  );
}
