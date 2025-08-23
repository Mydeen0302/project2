import '../static/homepage.css';
import { useEffect, useState } from 'react';

function HomePage() {
  const [user_id, setUserId] = useState('');
  const [datasets, saveDataset] = useState([]);
  const [file, newfile] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const id = localStorage.getItem('userid');

    if (!token) {
      window.location.href = '/';
      return;
    }

    setUserId(id);
    setIsLoading(false);

    fetch('/protected', {
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + token,
      },
    })
      .then(res => {
        if (res.status === 401) {
          alert('Unauthorized! Please log in again.');
          window.location.href = '/';
          return Promise.reject('Unauthorized');
        }
        return res.json();
      })
      .then(data => {
        if (data && data.message) {
          console.log(data.message);
        }
      })
      .catch(() => {
        alert('Error fetching protected data');
        window.location.href = '/';
      });
  }, []);

  useEffect(() => {
    if (!user_id) return;

    const token = localStorage.getItem('token');
    fetch(`/history?user_id=${user_id}`, {
      method: 'GET',
      headers: {
        Authorization: 'Bearer ' + token,
        'Content-Type': 'application/json',
      },
    })
      .then(async response => {
        if (!response.ok) {
          const errorData = await response.json();
          alert(errorData.message || 'Failed to fetch history');
          return;
        }
        const data = await response.json();
        saveDataset(data.datasets);
      })
      .catch(error => {
        console.error('Fetch failed:', error);
        alert(`Error fetching history: ${error.message || error}`);
      });

  }, [user_id]);

  const handleFileChange = (e) => {
    newfile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      alert('Please select a file');
      return;
    }

    const token = localStorage.getItem('token');
    const formdata = new FormData();
    formdata.append('file', file);
    formdata.append('user_id', user_id);

    try {
      const response = await fetch('/upload', {
        method: 'POST',
        headers: {
          Authorization: 'Bearer ' + token,
        },
        body: formdata,
      });

      if (!response.ok) {
        const errorData = await response.json();
        alert(errorData.message || 'Upload failed');
        return;
      }

      const data = await response.json();
      alert(data.message);

      const historyResponse = await fetch(`/history?user_id=${user_id}`, {
        method: 'GET',
        headers: {
          Authorization: 'Bearer ' + token,
          'Content-Type': 'application/json',
        },
      });

      if (!historyResponse.ok) {
        const Data = await historyResponse.json();
        console.error(Data.message)
        alert(Data.message || 'Failed to refresh history');
        return;
      }
      const historyData = await historyResponse.json();
      console.log(historyData);
      saveDataset(historyData.datasets);
    } catch (err) {
      alert('Upload failed or history fetch failed');
    }
  };

  if (isLoading) return null;

  return (
    <>
      <form onSubmit={handleSubmit} encType="multipart/form-data">
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Upload</button>
      </form>
      <div className='History'>
        <h1>History</h1>
        <table>
          <thead>
            <tr>
              <th>Dataset Name</th>
              <th>status</th>
              <th>Metrics</th>
            </tr>
          </thead>
         <tbody>
  {datasets.map(({ dataset_name, status_code, metrics }, index) => (
    <tr key={index}>
      <td>{dataset_name}</td>
      <td>{status_code}</td>
      <td>
        {metrics && Object.keys(metrics).length > 0 ? (
          <ul style={{ paddingLeft: '1rem', margin: 0 }}>
            {Object.entries(metrics).map(([key, value]) => (
              <li key={key}>
                <strong>{key}</strong>: {value}
              </li>
            ))}
          </ul>
        ) : (
          <em>No metrics</em>
        )}
      </td>
    </tr>
  ))}
  </tbody>
        </table>
      </div>
    </>
  );
}

export default HomePage;
