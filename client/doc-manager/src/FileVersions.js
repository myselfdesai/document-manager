import React, { useState, useEffect } from 'react';
import axios from 'axios';
import FileUploadForm from './components/FileUploadForm';


const FileVersions = () => {
  const [fileVersions, setFileVersions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchFileVersions = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost:8001/api/file_versions/', {
          headers: {
            Authorization: `Token ${token}`,
          },
        });
        setFileVersions(response.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching file versions:', error);
        setLoading(false);
      }
    };

    fetchFileVersions();
  }, []);

  const handleFileUploaded = (newFile) => {
    setFileVersions([...fileVersions, newFile]);
  };

  return (
    <div>
      <span className="text-light mr-3">Welcome to Document Management</span>
      <br></br>
      <h1>File Versions</h1>
      <FileUploadForm onFileUploaded={handleFileUploaded} />
      {loading ? (
        <p>Loading...</p>
      ) : (
        <ul>
          {fileVersions.map((fileVersion) => (
            <li key={fileVersion.id}>{fileVersion.file_name}</li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default FileVersions;