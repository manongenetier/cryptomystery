import React, { useState, useEffect } from "react";
import { cryptoApi } from "./services/cryptoApi";
import "./App.css";
import Typewriter from "./SplashScreen";

function App() {
  const [message, setMessage] = useState("");
  const [messageCode, setCode] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [paquet, setPaquet] = useState(null);
  const [splashDone, setSplashDone] = useState(false);

  const initPaquet = async () => {
    try {
      setLoading(true);
      const response = await cryptoApi.init();
      setPaquet(response);
      setError("");
    } catch (err) {
      setError("Erreur lors de l'initalisation du paquet");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    initPaquet();
  }, []);

  const handleCodage = async () => {
    if (!message.trim()) {
      setError("Entrez un message");
      return;
    }

    try {
      setLoading(true);
      const response = await cryptoApi.coder(message, paquet);
      setCode(response.result.join(","));
      setResult(`Message codé : ${response.result.join(",")}`);
      setError("");
    } catch (err) {
      setError("Codage echoué");
    } finally {
      setLoading(false);
    }
  };

  const handleDecodage = async () => {
    const codeArray = messageCode
      .split(",")
      .map((n) => parseInt(n.trim()))
      .filter((n) => !isNaN(n));

    try {
      setLoading(true);
      const response = await cryptoApi.decoder(codeArray, paquet);
      setResult(`Decodé : ${response.decode}`);
      setPaquet(response.etat_paquet);
      setError("");
    } catch (err) {
      setError("Decodage échoué");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <div id="intro" style={{ display: splashDone ? 'none' : 'flex' }}>
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

      {splashDone && (
        <>
          <div>
            <button onClick={initPaquet} disabled={loading}>
              Initialiser le paquet
            </button>
            {paquet && <p>Paquet initalisé</p>}
          </div>

          <div>
            <h3>coder</h3>
            <input
              type="text"
              placeholder="Message à coder"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              disabled={!paquet || loading}
            />
            <button onClick={handleCodage} disabled={!paquet || loading}>
              Coder
            </button>
            {messageCode && <p>message codé : {messageCode}</p>}
          </div>

          <div>
            <h3>Décoder</h3>
            <button
              onClick={handleDecodage}
              disabled={!paquet || loading || !messageCode}
            >
              Décoder
            </button>
            {result && <p>{result}</p>}
          </div>

          <div>
            <h3>État du paquet</h3>
            {paquet &&
              paquet.map((carte, index) => (
                <p key={index}>
                  {carte.carte} : {carte.valeur}
                </p>
              ))}
          </div>
        </>
      )}
    </div>
  );
}

export default App;