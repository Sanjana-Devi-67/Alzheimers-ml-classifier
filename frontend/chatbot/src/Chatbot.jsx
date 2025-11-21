
import React, { useState, useRef, useEffect } from "react";

const BACKEND_URL = "http://127.0.0.1:8000/message";

const UPLOAD_URL = "http://127.0.0.1:8000/upload";

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [uploading, setUploading] = useState(false);
  const [typing, setTyping] = useState(false);
  const [open, setOpen] = useState(false);
  const [showBubble, setShowBubble] = useState(true);
  const fileInputRef = useRef(null);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, typing]);

  const handleSend = async () => {
    if (!input.trim()) return;

    setMessages((prev) => [...prev, { sender: "user", text: input }]);
    const userMessage = input;
    setInput("");
    setTyping(true);

    try {
      const res = await fetch(BACKEND_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: userMessage }),
      });
      const data = await res.json();

      setTimeout(() => {
        setMessages((prev) => [
          ...prev,
          { sender: "bot", text: data.response },
        ]);
        setTyping(false);
      }, 500);
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "Oops! Something went wrong." },
      ]);
      setTyping(false);
    }
  };

  const handleUploadClick = () => fileInputRef.current.click();

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setUploading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(UPLOAD_URL, { method: "POST", body: formData });
      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        { sender: "user", text: `Uploaded file: ${file.name}` },
        { sender: "bot", text: data.excerpt || "File uploaded!" },
      ]);
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "Upload failed!" },
      ]);
    } finally {
      setUploading(false);
    }
  };

  return (
    <>
      {/* 🧠 Floating Robot Button + “Here to Talk” Bubble */}
      <div
        style={{
          position: "fixed",
          bottom: "24px",
          right: "24px",
          zIndex: 1000,
          display: "flex",
          alignItems: "center",
          gap: "10px",
        }}
      >
        {/* Speech Bubble */}
        {showBubble && !open && (
          <div
            style={{
              background: "#ffffff",
              color: "#000",
              border: "1px solid #90caf9",
              padding: "8px 12px",
              borderRadius: "16px",
              fontSize: "14px",
              boxShadow: "0 4px 10px rgba(0,0,0,0.1)",
              animation: "fadeIn 0.6s ease",
              fontWeight: 500,
            }}
          >
            💬 Here to talk!
          </div>
        )}

        {/* Floating Robot Button */}
        <button
          onClick={() => {
            setOpen(!open);
            setShowBubble(false);
          }}
          style={{
            width: "70px",
            height: "70px",
            borderRadius: "50%",
            background: open
              ? "radial-gradient(circle at 30% 30%, #bbdefb, #64b5f6, #1e88e5)"
              : "radial-gradient(circle at 30% 30%, #64b5f6, #2196f3, #1565c0)",
            border: "2px solid #fff",
            boxShadow: open
              ? "0 0 20px rgba(30,136,229,0.4)"
              : "0 0 35px rgba(33,150,243,0.8)",
            cursor: "pointer",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: "34px",
            color: "#fff",
            animation: open ? "none" : "floatPulse 2.5s ease-in-out infinite",
            transition: "all 0.3s ease",
          }}
          onMouseEnter={(e) =>
            (e.currentTarget.style.transform = "scale(1.1)")
          }
          onMouseLeave={(e) =>
            (e.currentTarget.style.transform = "scale(1)")
          }
        >
          {!open ? "🤖" : "✕"}
        </button>

        <style>{`
          @keyframes floatPulse {
            0% { transform: translateY(0px); box-shadow: 0 0 20px rgba(33,150,243,0.6); }
            50% { transform: translateY(-5px); box-shadow: 0 0 35px rgba(33,150,243,0.9); }
            100% { transform: translateY(0px); box-shadow: 0 0 20px rgba(33,150,243,0.6); }
          }
          @keyframes fadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
          }
        `}</style>
      </div>

      {/* 💬 Chat Window */}
      {open && (
        <div
          style={{
            position: "fixed",
            bottom: "100px",
            right: "24px",
            width: "380px",
            maxHeight: "540px",
            background: "#ffffff",
            borderRadius: "20px",
            boxShadow: "0 10px 25px rgba(0,0,0,0.25)",
            display: "flex",
            flexDirection: "column",
            padding: "14px",
            fontFamily: "'Poppins', sans-serif",
            zIndex: 999,
          }}
        >
          <div
            style={{
              flex: 1,
              overflowY: "auto",
              padding: "10px",
              background: "linear-gradient(135deg, #e3f2fd, #f8fbff)",
              borderRadius: "12px",
            }}
          >
            {messages.map((msg, idx) => (
              <div
                key={idx}
                style={{
                  display: "flex",
                  justifyContent:
                    msg.sender === "user" ? "flex-end" : "flex-start",
                  margin: "8px 0",
                  animation: "fadeIn 0.4s ease",
                }}
              >
                <span
                  style={{
                    background:
                      msg.sender === "user"
                        ? "#64b5f6"
                        : "rgba(255,255,255,0.9)",
                    color: msg.sender === "user" ? "#fff" : "#000",
                    padding: "10px 16px",
                    borderRadius: "20px",
                    maxWidth: "80%",
                    wordBreak: "break-word",
                    boxShadow:
                      msg.sender === "user"
                        ? "0 4px 10px rgba(100,181,246,0.4)"
                        : "0 3px 8px rgba(0,0,0,0.1)",
                  }}
                >
                  {msg.text}
                </span>
              </div>
            ))}

            {typing && (
              <div style={{ display: "flex", margin: "6px 0" }}>
                <span
                  style={{
                    background: "rgba(255,255,255,0.9)",
                    padding: "10px 16px",
                    borderRadius: "20px",
                    display: "flex",
                    gap: "4px",
                  }}
                >
                  {[0, 1, 2].map((i) => (
                    <span
                      key={i}
                      style={{
                        width: "6px",
                        height: "6px",
                        background: "#000",
                        borderRadius: "50%",
                        animation: `bounce 1s infinite ${i * 0.2}s`,
                      }}
                    ></span>
                  ))}
                </span>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>

          <div style={{ display: "flex", marginTop: "10px" }}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              style={{
                flex: 1,
                padding: "10px 14px",
                borderRadius: "24px",
                border: "1px solid #90caf9",
                outline: "none",
                color: "#000",
              }}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
            />
            <button
              onClick={handleSend}
              style={{
                marginLeft: "8px",
                padding: "10px 14px",
                borderRadius: "50%",
                border: "none",
                background: "#1e88e5",
                color: "#fff",
                cursor: "pointer",
                transition: "transform 0.2s",
              }}
              onMouseEnter={(e) =>
                (e.currentTarget.style.transform = "scale(1.1)")
              }
              onMouseLeave={(e) =>
                (e.currentTarget.style.transform = "scale(1)")
              }
            >
              ➤
            </button>
            <button
              onClick={handleUploadClick}
              style={{
                marginLeft: "6px",
                padding: "10px 14px",
                borderRadius: "50%",
                border: "none",
                background: "#e3f2fd",
                cursor: "pointer",
                color: "#000",
              }}
            >
              📎
            </button>
            <input
              type="file"
              ref={fileInputRef}
              style={{ display: "none" }}
              onChange={handleFileChange}
            />
          </div>

          {uploading && (
            <div
              style={{
                textAlign: "center",
                marginTop: "5px",
                fontSize: "12px",
                color: "#555",
              }}
            >
              Uploading...
            </div>
          )}

          <style>{`
            @keyframes bounce {
              0%, 80%, 100% { transform: scale(0); }
              40% { transform: scale(1); }
            }
          `}</style>
        </div>
      )}
    </>
  );
};

export default Chatbot;
