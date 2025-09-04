import React from "react";
import "./CMH.css";

const CMHTimeline = ({ timeline }) => {
  return (
    <div className="timeline-container">
      <h2>Clinical History Timeline</h2>
      <div className="timeline">
        {timeline && timeline.length > 0 ? (
          timeline.map((item, index) => (
            <div key={index} className="timeline-item">
              <div className="timeline-date">{item.date}</div>
              <div className="timeline-content">
                <h3>{item.title}</h3>
                <p>{item.description}</p>
                {item.doctor && <span>Doctor: {item.doctor}</span>}
                {item.notes && <p className="notes">Notes: {item.notes}</p>}
              </div>
            </div>
          ))
        ) : (
          <p>No records found</p>
        )}
      </div>
    </div>
  );
};

export default CMHTimeline;
