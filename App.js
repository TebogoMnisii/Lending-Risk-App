import React, { useState } from "react";
import { Doughnut } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { CSVLink } from "react-csv";
import {
  FaUserTie,
  FaMoneyBillWave,
  FaHome,
  FaUniversity,
  FaRedo,
  FaChild,
  FaBriefcase,
} from "react-icons/fa";
import "./App.css";

ChartJS.register(ArcElement, Tooltip, Legend);

export default function App() {
  const [formData, setFormData] = useState({
    employment_status: "Employed",
    monthly_income: "",
    monthly_rent: "",
    has_bank_account: 1,
    repaid_previous_loans: 1,
    last_loan_amount_repaid: "",
    number_of_dependents: "",
    business_years: "",
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const statuses = ["Employed", "Self-Employed", "Unemployed", "Student"];

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "number" ? Number(value) : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    try {
      const response = await fetch("https://loan-risk-api.onrender.com/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      alert("Error: " + error.message);
    }
    setLoading(false);
  };

  const handleReset = () => {
    setResult(null);
    setFormData({
      employment_status: "Employed",
      monthly_income: "",
      monthly_rent: "",
      has_bank_account: 1,
      repaid_previous_loans: 1,
      last_loan_amount_repaid: "",
      number_of_dependents: "",
      business_years: "",
    });
  };

  const confidence = result ? Math.round(result.confidence) : 0;

  const data = {
    labels: ["Confidence", "Remaining"],
    datasets: [
      {
        data: [confidence, 100 - confidence],
        backgroundColor: ["#007bff", "#e0e0e0"],
        borderWidth: 0,
        hoverOffset: 10,
      },
    ],
  };

  const csvData = result
    ? [
        {
          ...formData,
          prediction: result.prediction,
          confidence: result.confidence,
        },
      ]
    : [];

  return (
    <div className="container">
      <h2>Loan Default Risk Prediction</h2>

      {!result && (
        <form onSubmit={handleSubmit}>
          <label>
            <FaUserTie style={{ marginRight: "6px" }} />
            Employment Status:
            <select
              name="employment_status"
              value={formData.employment_status}
              onChange={handleChange}
              required
            >
              {statuses.map((status) => (
                <option key={status} value={status}>
                  {status}
                </option>
              ))}
            </select>
          </label>

          <label>
            <FaMoneyBillWave style={{ marginRight: "6px" }} />
            Monthly Income:
            <input
              type="number"
              name="monthly_income"
              value={formData.monthly_income}
              onChange={handleChange}
              required
              min="0"
              step="any"
            />
          </label>

          <label>
            <FaHome style={{ marginRight: "6px" }} />
            Monthly Rent:
            <input
              type="number"
              name="monthly_rent"
              value={formData.monthly_rent}
              onChange={handleChange}
              required
              min="0"
              step="any"
            />
          </label>

          <label>
            <FaUniversity style={{ marginRight: "6px" }} />
            Has Bank Account:
            <select
              name="has_bank_account"
              value={formData.has_bank_account}
              onChange={handleChange}
            >
              <option value={1}>Yes</option>
              <option value={0}>No</option>
            </select>
          </label>

          <label>
            <FaRedo style={{ marginRight: "6px" }} />
            Repaid Previous Loans:
            <select
              name="repaid_previous_loans"
              value={formData.repaid_previous_loans}
              onChange={handleChange}
            >
              <option value={1}>Yes</option>
              <option value={0}>No</option>
            </select>
          </label>

          <label>
            <FaMoneyBillWave style={{ marginRight: "6px" }} />
            Last Loan Amount Repaid:
            <input
              type="number"
              name="last_loan_amount_repaid"
              value={formData.last_loan_amount_repaid}
              onChange={handleChange}
              min="0"
              step="any"
              required
            />
          </label>

          <label>
            <FaChild style={{ marginRight: "6px" }} />
            Number of Dependents:
            <input
              type="number"
              name="number_of_dependents"
              value={formData.number_of_dependents}
              onChange={handleChange}
              min="0"
              required
            />
          </label>

          <label>
            <FaBriefcase style={{ marginRight: "6px" }} />
            Years in Business:
            <input
              type="number"
              name="business_years"
              value={formData.business_years}
              onChange={handleChange}
              min="0"
              step="any"
              required
            />
          </label>

          <button type="submit" disabled={loading}>
            {loading ? "Predicting..." : "Predict"}
          </button>
        </form>
      )}

      {result && (
        <div className="result fade-in">
          <h3>
            Prediction:{" "}
            <span
              style={{
                color: confidence > 50 ? "red" : "green",
                fontWeight: "bold",
              }}
            >
              {result.prediction}
            </span>
          </h3>

          <div className="chart-wrapper">
            <Doughnut data={data} />
          </div>

          <p>Confidence: {confidence}%</p>

          <div style={{ marginTop: "1em" }}>
            <CSVLink data={csvData} filename="prediction_result.csv">
              <button>Download as CSV</button>
            </CSVLink>
          </div>

          <button onClick={handleReset} style={{ marginTop: "1em" }}>
            Try Again
          </button>
        </div>
      )}
    </div>
  );
}


