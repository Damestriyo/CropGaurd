import { useEffect, useState } from "react";
import "./index.css";
import { analyzeLeaf, getHealth } from "./api";

function App() {
  const [image, setImage] = useState(null);
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [apiStatus, setApiStatus] = useState("checking");

  useEffect(() => {
    getHealth()
      .then(() => setApiStatus("online"))
      .catch(() => setApiStatus("offline"));
  }, []);

  const handleImage = (event) => {
    const selectedFile = event.target.files[0];

    if (selectedFile) {
      setFile(selectedFile);
      setImage(URL.createObjectURL(selectedFile));
      setResult(null);
      setError("");
    }
  };

  const analyzeImage = async () => {
    if (!file) {
      alert("Please upload a leaf image first.");
      return;
    }

    setLoading(true);
    setError("");
    try {
      const response = await analyzeLeaf(file);
      setResult(response);
      setApiStatus("online");
    } catch (requestError) {
      setError(requestError.message || "The image could not be analyzed. Please try again.");
      setApiStatus("offline");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">

      {/* NAVBAR */}
      <nav className="navbar">

        <div className="logo">
          🌱 <span>CropGuard</span>
        </div>

        <div className={`api-status api-status-${apiStatus}`} role="status">
          <span /> API {apiStatus === "checking" ? "connecting" : apiStatus}
        </div>

        <div className="nav-links">
          <a href="#home">Home</a>
          <a href="#detect">Detect</a>
          <a href="#about">About</a>
        </div>

        <a href="#detect" className="nav-button">
          Start Detection
        </a>

      </nav>


      {/* HERO */}
      <section className="hero" id="home">

        <div className="hero-content">

          <div className="badge">
            🌿 AI POWERED AGRICULTURE
          </div>

          <h1>
            Detect Crop
            <br />
            Diseases <span>Instantly.</span>
          </h1>

          <p>
            Upload a photo of a crop leaf and our AI-powered
            system analyzes it to identify diseases and provide
            useful treatment information.
          </p>

          <div className="hero-buttons">

            <a href="#detect" className="primary-button">
              Detect Disease →
            </a>

            <a href="#about" className="secondary-button">
              Learn More
            </a>

          </div>

        </div>


        <div className="hero-visual">

          <div className="plant-circle">
            🌿
          </div>

          <div className="floating-card card-one">
            ✓ AI Detection
          </div>

          <div className="floating-card card-two">
            📊 94.6% Confidence
          </div>

        </div>

      </section>


      {/* DETECTION SECTION */}
      <section className="detect-section" id="detect">

        <div className="section-title">

          <div className="small-title">
            AI DISEASE DETECTION
          </div>

          <h2>
            Analyze Your Crop
          </h2>

          <p>
            Upload a clear image of a crop leaf to begin analysis.
          </p>

        </div>


        <div className="upload-area">

          <div className="upload-box">

            {image ? (

              <img
                src={image}
                alt="Selected leaf"
                className="preview-image"
              />

            ) : (

              <>
                <div className="upload-icon">
                  📷
                </div>

                <h3>
                  Upload Leaf Image
                </h3>

                <p>
                  Drag and drop your image here
                  <br />
                  or select a file from your device
                </p>
              </>

            )}


            <label className="upload-button">

              {image ? "Choose Another Image" : "Choose Image"}

              <input
                type="file"
                accept="image/png,image/jpeg,image/webp"
                onChange={handleImage}
                hidden
              />

            </label>


            {image && (

              <button
                className="analyze-button"
                onClick={analyzeImage}
                disabled={loading}
              >

                {loading
                  ? "Analyzing..."
                  : "🔍 Analyze Leaf"}

              </button>

            )}

          </div>

        </div>


        {/* RESULT */}
        {error && <div className="error-message" role="alert">{error}</div>}

        {result && (

          <div className="result-card">

            <div className="result-top">

              <div>
                <div className="result-label">
                  AI DIAGNOSIS RESULT
                </div>

                <h2>
                  {result.prediction.disease}
                </h2>
              </div>

              <div className="healthy-status">
                {result.prediction.is_healthy ? "✓ Healthy Leaf" : "⚠ Disease Detected"}
              </div>

            </div>


            <div className="result-stats">

              <div className="stat">
                <span>Crop</span>
                <strong>
                  {result.prediction.crop}
                </strong>
              </div>

              <div className="stat">
                <span>Confidence</span>
                <strong>
                  {Number(result.prediction.confidence).toFixed(2)}%
                </strong>
              </div>

              <div className="stat">
                <span>Severity</span>
                <strong>
                  {result.prediction.severity}
                </strong>
              </div>

            </div>


            <div className="result-info">

              <div className="info-box">

                <h3>
                  🩺 Symptoms
                </h3>

                <p>{result.disease_info?.symptoms?.length
                  ? result.disease_info.symptoms.join(" ")
                  : "No additional symptom information is available for this diagnosis."}</p>

              </div>


              <div className="info-box">

                <h3>
                  🛡️ Recommended Management
                </h3>

                <p>{result.disease_info?.management?.length
                  ? result.disease_info.management.join(" ")
                  : result.disease_info?.prevention?.join(" ") || "Follow local agricultural guidance for this crop."}</p>

              </div>

            </div>

          </div>

        )}

      </section>


      {/* FEATURES */}
      <section className="features">

        <div className="feature-card">

          <div className="feature-icon">
            🔍
          </div>

          <h3>
            AI Detection
          </h3>

          <p>
            Analyze leaf images and identify potential
            crop diseases.
          </p>

        </div>


        <div className="feature-card">

          <div className="feature-icon">
            📊
          </div>

          <h3>
            Confidence Score
          </h3>

          <p>
            Get a confidence score along with your
            disease prediction.
          </p>

        </div>


        <div className="feature-card">

          <div className="feature-icon">
            🌱
          </div>

          <h3>
            Treatment Guidance
          </h3>

          <p>
            Understand symptoms and learn about
            possible management methods.
          </p>

        </div>

      </section>


      {/* ABOUT */}
      <section className="about" id="about">

        <div>

          <div className="small-title">
            ABOUT THE PROJECT
          </div>

          <h2>
            Making Crop Health
            <br />
            Smarter With AI
          </h2>

          <p>
            CropGuard is an AI-based crop disease detection
            system designed to help identify diseases from
            crop leaf images.
          </p>

        </div>

        <div className="about-box">

          <div>
            <strong>AI</strong>
            <span>Powered</span>
          </div>

          <div>
            <strong>Fast</strong>
            <span>Detection</span>
          </div>

          <div>
            <strong>Easy</strong>
            <span>To Use</span>
          </div>

        </div>

      </section>


      {/* FOOTER */}
      <footer>

        <div className="footer-logo">
          🌱 CropGuard
        </div>

        <p>
          AI Based Crop Disease Detection System
        </p>

        <p className="copyright">
          © 2026 CropGuard • School Project
        </p>

      </footer>

    </div>
  );
}

export default App;
