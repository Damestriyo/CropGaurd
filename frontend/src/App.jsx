import { useEffect, useState } from "react";
import "./index.css";
import { analyzeLeaf, getHealth } from "./api";
import { getLeafConfirmationError } from "./leafConfirmation";

const ACCEPTED_IMAGE_TYPES = new Set(["image/jpeg", "image/png", "image/webp"]);
const ACCEPTED_IMAGE_EXTENSIONS = new Set(["jpg", "jpeg", "png", "webp"]);
// Matches the backend's configured default; MAX_IMAGE_SIZE_MB can override it there.
const MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024;

function getFileError(file) {
  if (!file) return "Please upload a leaf image first.";

  const extension = file.name.split(".").pop()?.toLowerCase();
  const mimeType = file.type.toLowerCase();
  if (
    !ACCEPTED_IMAGE_EXTENSIONS.has(extension) ||
    (mimeType && !ACCEPTED_IMAGE_TYPES.has(mimeType))
  ) {
    return "Choose a JPEG, PNG, or WEBP image.";
  }
  if (file.size > MAX_IMAGE_SIZE_BYTES) {
    return "The image must be 10 MB or smaller.";
  }

  return "";
}

function InfoList({ items, fallback }) {
  if (!Array.isArray(items) || items.length === 0) {
    return <p className="info-fallback">{fallback}</p>;
  }

  return (
    <ul className="info-list">
      {items.map((item, index) => (
        <li key={`${index}-${item}`}>{item}</li>
      ))}
    </ul>
  );
}

function App() {
  const [image, setImage] = useState(null);
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [apiStatus, setApiStatus] = useState("checking");
  const [isDragging, setIsDragging] = useState(false);
  const [leafConfirmed, setLeafConfirmed] = useState(false);

  useEffect(() => {
    getHealth()
      .then(() => setApiStatus("online"))
      .catch(() => setApiStatus("offline"));
  }, []);

  const handleImage = (selectedFile) => {
    const fileError = getFileError(selectedFile);
    if (fileError) {
      setError(fileError);
      return;
    }

    setFile(selectedFile);
    setImage(URL.createObjectURL(selectedFile));
    setResult(null);
    setLeafConfirmed(false);
    setError("");
  };

  const handleDragOver = (event) => {
    event.preventDefault();
    if (Array.from(event.dataTransfer.types).includes("Files")) {
      event.dataTransfer.dropEffect = "copy";
    }
  };

  const handleDragEnter = (event) => {
    event.preventDefault();
    if (Array.from(event.dataTransfer.types).includes("Files")) {
      setIsDragging(true);
    }
  };

  const handleDragLeave = (event) => {
    event.preventDefault();
    if (!event.currentTarget.contains(event.relatedTarget)) {
      setIsDragging(false);
    }
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setIsDragging(false);
    const droppedFile = event.dataTransfer.files?.[0];
    if (!droppedFile) {
      setError("Drop a JPEG, PNG, or WEBP image to continue.");
      return;
    }
    handleImage(droppedFile);
  };

  const analyzeImage = async () => {
    const fileError = getFileError(file);
    if (fileError) {
      setError(fileError);
      return;
    }
    const confirmationError = getLeafConfirmationError(leafConfirmed);
    if (confirmationError) {
      setError(confirmationError);
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

          <div
            className={`upload-box${isDragging ? " upload-box-dragging" : ""}`}
            onDragOver={handleDragOver}
            onDragEnter={handleDragEnter}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            role="group"
            aria-label="Image upload area"
          >

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
                  or select a file from your device (JPEG, PNG, or WEBP; up to 10 MB)
                </p>
              </>

            )}


            <label className="upload-button">

              {image ? "Choose Another Image" : "Choose Image"}

              <input
                className="file-input"
                type="file"
                accept="image/png,image/jpeg,image/webp"
                aria-label="Choose a leaf image"
                onChange={(event) => {
                  if (event.target.files?.[0]) {
                    handleImage(event.target.files[0]);
                  }
                  event.target.value = "";
                }}
              />

            </label>

            <p className="image-scope-note" id="image-scope-note">
              This classifier is trained for crop-leaf images and does not verify image content. Other photos can receive confident but incorrect disease labels.
            </p>

            {image && (
              <label className="leaf-confirmation">
                <input
                  type="checkbox"
                  checked={leafConfirmed}
                  onChange={(event) => setLeafConfirmed(event.target.checked)}
                  aria-describedby="image-scope-note"
                />
                <span>I confirm the image's main subject is a crop leaf.</span>
              </label>
            )}


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

          <span className="sr-only" role="status">
            {isDragging ? "Release to upload the image." : ""}
          </span>

        </div>


        {/* RESULT */}
        {error && <div className="error-message" role="alert">{error}</div>}

        {result && (

          <div className="result-card">

            <div className="result-heading">
              <div className="result-label">AI DIAGNOSIS RESULT</div>
              <p>Review the prediction and care information for this leaf.</p>
            </div>

            <div className="result-top">

              <div>
                <h2>
                  {result.prediction.disease}
                </h2>
              </div>

              <div className={`healthy-status${result.prediction.is_healthy ? " healthy" : ""}`}>
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
                <span>Individual plant severity</span>
                <strong>
                  {result.prediction.severity?.toLowerCase() === "unknown"
                    ? "Not assessed"
                    : result.prediction.severity ?? "Not assessed"}
                </strong>
              </div>

              {result.disease_info?.severity && (
                <div className="stat stat-typical-severity">
                  <span>Typical disease severity</span>
                  <strong>{result.disease_info.severity}</strong>
                </div>
              )}

            </div>


            <div className="result-info">

              <div className="info-box">

                <h3>
                  🩺 Symptoms
                </h3>

                <InfoList
                  items={result.disease_info?.symptoms}
                  fallback="No additional symptom information is available for this diagnosis."
                />

              </div>


              <div className="info-box">

                <h3>
                  🔎 Causes
                </h3>

                <InfoList
                  items={result.disease_info?.causes}
                  fallback="No cause information is available for this diagnosis."
                />

              </div>


              <div className="info-box">

                <h3>
                  🛡️ Prevention
                </h3>

                <InfoList
                  items={result.disease_info?.prevention}
                  fallback="No prevention information is available for this diagnosis."
                />

              </div>


              <div className="info-box">

                <h3>
                  🛡️ Recommended Management
                </h3>

                <InfoList
                  items={result.disease_info?.management?.length
                    ? result.disease_info.management
                    : result.disease_info?.prevention}
                  fallback="Follow local agricultural guidance for this crop."
                />

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
