import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import JobGraphs from "./components/GraphComponent";
import JobForm from "./components/JobForm/JobForm";

function App() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);

  const fetchJobs = async () => {
    const res = await fetch("http://localhost:8000/jobs/");
    const data = await res.json();
    setJobs(data);
  };

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await fetch('http://localhost:8000/jobs/');
        const data = await response.json();
        setJobs(data);
      } catch (error) {
        console.error('Error fetching jobs:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchJobs();
  }, []);

  return (
    <div className="App">
      {loading && <p>Loading...</p>}
      <button onClick={() => setShowModal(true)} style={{ marginBottom: "1rem" }}>
        + Add Job
      </button>

      {showModal && (
        <JobForm
          onClose={() => setShowModal(false)}
          onJobAdded={fetchJobs}
        />
      )}

      {!loading && jobs.length > 0 && <JobGraphs jobData={jobs} />}
    </div>
  );
}


export default App
