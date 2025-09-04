import React, { useEffect, useState } from "react";
import { patientLabResultsAPI } from "../services/apis/patientLabResultsAPI"; // We'll create this API service
import { Download } from "lucide-react";

const PatientLabResultsPage = () => {
  const [labResults, setLabResults] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLabResults();
  }, []);

  const fetchLabResults = async () => {
    try {
      setLoading(true);
      const data = await patientLabResultsAPI.getMyLabResults();
      setLabResults(data);
    } catch (error) {
      console.error("Error fetching lab results:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async (id) => {
    try {
      const pdfBlob = await patientLabResultsAPI.downloadPdf(id);
      const url = window.URL.createObjectURL(new Blob([pdfBlob]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `lab-result-${id}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error("Download failed:", error);
    }
  };

  const filteredResults = labResults.filter((result) =>
    result.testName.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">My Lab Results</h1>

      {/* Search */}
      <div className="mb-4">
        <input
          type="text"
          placeholder="Search by test name..."
          className="border border-gray-300 rounded px-3 py-2 w-full md:w-1/3"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {loading ? (
        <p>Loading...</p>
      ) : (
        <div className="overflow-x-auto bg-white rounded shadow">
          <table className="w-full border-collapse">
            <thead>
              <tr className="bg-gray-100 text-left">
                <th className="p-3 border-b">Test Name</th>
                <th className="p-3 border-b">Date</th>
                <th className="p-3 border-b">Status</th>
                <th className="p-3 border-b">Action</th>
              </tr>
            </thead>
            <tbody>
              {filteredResults.length > 0 ? (
                filteredResults.map((result) => (
                  <tr key={result.id} className="hover:bg-gray-50">
                    <td className="p-3 border-b">{result.testName}</td>
                    <td className="p-3 border-b">{result.date}</td>
                    <td className="p-3 border-b">
                      <span
                        className={`px-2 py-1 rounded text-sm ${
                          result.status === "Completed"
                            ? "bg-green-100 text-green-700"
                            : "bg-yellow-100 text-yellow-700"
                        }`}
                      >
                        {result.status}
                      </span>
                    </td>
                    <td className="p-3 border-b">
                      <button
                        onClick={() => handleDownload(result.id)}
                        className="flex items-center gap-2 text-blue-600 hover:underline"
                      >
                        <Download size={16} /> Download
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="4" className="text-center p-4">
                    No lab results found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default PatientLabResultsPage;
