import { useEffect, useState } from "react";
import { prescriptionsAPI } from "../services/apis/prescriptions.js";
import "../pages/Dashboard/Dashboard.css";


const PatientPrescriptionsPage = () => {
  const [prescriptions, setPrescriptions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [downloadingId, setDownloadingId] = useState(null);

  useEffect(() => {
    const loadPrescriptions = async () => {
      setLoading(true);
      try {
        const data = await prescriptionsAPI.getMyPrescriptions();
        setPrescriptions(data);
      } catch (err) {
        console.error("Failed to load prescriptions", err);
        alert("Failed to load prescriptions. Check console for details.");
      } finally {
        setLoading(false);
      }
    };
    loadPrescriptions();
  }, []);

  const handleDownload = async (id, filename) => {
    try {
      setDownloadingId(id);
      const blob = await prescriptionsAPI.downloadPdf(id);
      const url = window.URL.createObjectURL(new Blob([blob], { type: "application/pdf" }));
      const a = document.createElement("a");
      a.href = url;
      a.download = filename || `prescription-${id}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Download error", err);
      alert("Failed to download PDF.");
    } finally {
      setDownloadingId(null);
    }
  };

  if (loading) {
    return (
      <div className="dashboard">
        <h2>My Prescriptions</h2>
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <h2>My Prescriptions</h2>

      {prescriptions.length === 0 ? (
        <div className="card">
          <p>No prescriptions found.</p>
        </div>
      ) : (
        <ul className="prescription-list">
          {prescriptions.map((p) => {
            const docs = p.items || [];
            const doctorName = p.doctor_name || p.doctor?.user?.full_name || "Doctor";
            const createdAt = p.created_at ? new Date(p.created_at).toLocaleString() : "";

            return (
              <li key={p.id} className="prescription-item card">
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <div>
                    <strong>Prescription #{p.id}</strong>
                    <div style={{ fontSize: 13, color: "#666" }}>
                      <span>Dr. {doctorName}</span> • <span>{createdAt}</span>
                    </div>
                  </div>
                  <div>
                    <button
                      className="btn btn-sm btn-primary"
                      onClick={() => handleDownload(p.id, `prescription-${p.id}.pdf`)}
                      disabled={downloadingId === p.id}
                    >
                      {downloadingId === p.id ? "Downloading..." : "Download PDF"}
                    </button>
                  </div>
                </div>

                <div style={{ marginTop: 10 }}>
                  <strong>Items:</strong>
                  <ul>
                    {docs.map((it, idx) => (
                      <li key={idx}>
                        {it.drug || it.name} — {it.dosage || it.dose || ""}{" "}
                        {it.frequency ? ` — ${it.frequency}` : ""}{" "}
                        {it.duration ? ` — ${it.duration}` : ""}{" "}
                        {it.notes ? ` (${it.notes})` : ""}
                      </li>
                    ))}
                  </ul>
                </div>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
};

export default PatientPrescriptionsPage;
