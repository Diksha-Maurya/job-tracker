import { useEffect, useState } from "react";
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
} from "chart.js";
import { Bar, Line } from "react-chartjs-2";

ChartJS.register(
  BarElement,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend
);

function JobGraphs({ jobData }) {
  const [filter, setFilter] = useState("7days");
  const [filteredData, setFilteredData] = useState([]);

  useEffect(() => {
    const now = new Date();
    let cutoff = new Date();

    if (filter === "today") {
      cutoff.setHours(0, 0, 0, 0);
    } else if (filter === "7days") {
      cutoff.setDate(now.getDate() - 7);
    } else if (filter === "1month") {
      cutoff.setMonth(now.getMonth() - 1);
    }

    const result = jobData.filter((job) => {
      const appliedDate = new Date(job.applied_on);
      return appliedDate >= cutoff;
    });

    setFilteredData(result);
  }, [filter, jobData]);

  const getChartData = () => {
    const now = new Date();
    let startDate = new Date();
  
    if (filter === "today") {
      const statusCount = filteredData.reduce((acc, job) => {
        acc[job.status] = (acc[job.status] || 0) + 1;
        return acc;
      }, {});
  
      return {
        type: "bar",
        data: {
          labels: Object.keys(statusCount),
          datasets: [
            {
              label: `Applications (${filter})`,
              data: Object.values(statusCount),
              backgroundColor: "rgba(54, 162, 235, 0.6)",
            },
          ],
        },
      };
    } else {
      if (filter === "7days") {
        startDate.setDate(now.getDate() - 6); // include today
      } else if (filter === "1month") {
        startDate.setDate(now.getDate() - 29);
      }
  
      const allDates = [];
      for (let d = new Date(startDate); d <= now; d.setDate(d.getDate() + 1)) {
        allDates.push(new Date(d).toISOString().split("T")[0]);
      }
  
      const dateCount = {};
      filteredData.forEach((job) => {
        const date = new Date(job.applied_on).toISOString().split("T")[0];
        dateCount[date] = (dateCount[date] || 0) + 1;
      });
  
      const labels = allDates;
      const values = allDates.map((date) => dateCount[date] || 0);
  
      return {
        type: "line",
        data: {
          labels,
          datasets: [
            {
              label: `Applications (${filter})`,
              data: values,
              fill: false,
              borderColor: "rgba(75,192,192,1)",
              backgroundColor: "rgba(75,192,192,0.4)",
              tension: 0.3,
            },
          ],
        },
      };
    }
  };
  

  const chart = getChartData();

  const options = {
    responsive: true,
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 1,
          precision: 0,
          callback: function (value) {
            return Number.isInteger(value) ? value : null;
          },
        },
      },
    },
  };

  return (
    <div style={{ height: "900px", width: "1000px" }}>
      <h2>Job Applications</h2>
      <select value={filter} onChange={(e) => setFilter(e.target.value)}>
        <option value="today">Today</option>
        <option value="7days">Last 7 Days</option>
        <option value="1month">Last 1 Month</option>
      </select>

      <div style={{ height: "900px", width: "100%" }}>
    {chart.type === "bar" ? (
      <Bar data={chart.data} options={{ ...options, responsive: true }} />
    ) : (
      <Line data={chart.data} options={{ ...options, responsive: true }} />
    )}
  </div>
    </div>
  );
}

export default JobGraphs;
