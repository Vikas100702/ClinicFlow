import { useState } from "react";
import { prescriptionsAPI } from "../services/apis/prescriptions";
import { toast } from "react-toastify";

const CreatePrescriptionPage = ({ appointmentId }) => {
  const [items, setItems] = useState([{ drug: "", dosage: "", frequency: "", duration: "" }]);
  const [loading, setLoading] = useState(false);

  const handleChange = (index, field, value) => {
    const newItems = [...items];
    newItems[index][field] = value;
    setItems(newItems);
  };

  const addItem = () => setItems([...items, { drug: "", dosage: "", frequency: "", duration: "" }]);

  const validateItems = () => {
    return items.every((item) => item.drug.trim() && item.dosage.trim());
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateItems()) {
      toast.error("Please fill drug name and dosage for all items.");
      return;
    }
    setLoading(true);
    try {
      await prescriptionsAPI.create({ appointment_id: appointmentId, items });
      toast.success("Prescription created successfully!");
      setItems([{ drug: "", dosage: "", frequency: "", duration: "" }]);
    } catch (err) {
      console.error(err);
      toast.error("Failed to create prescription");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Create Prescription</h2>
      <form onSubmit={handleSubmit}>
        {items.map((item, i) => (
          <div key={i} style={{ marginBottom: 10 }}>
            <input placeholder="Drug" value={item.drug} onChange={(e) => handleChange(i, "drug", e.target.value)} />
            <input placeholder="Dosage" value={item.dosage} onChange={(e) => handleChange(i, "dosage", e.target.value)} />
            <input placeholder="Frequency" value={item.frequency} onChange={(e) => handleChange(i, "frequency", e.target.value)} />
            <input placeholder="Duration" value={item.duration} onChange={(e) => handleChange(i, "duration", e.target.value)} />
          </div>
        ))}
        <button type="button" onClick={addItem}>+ Add Medicine</button>
        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? "Saving..." : "Save Prescription"}
        </button>
      </form>
    </div>
  );
};

export default CreatePrescriptionPage;
