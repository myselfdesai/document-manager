import React, { useState, useEffect } from 'react';
import axios from 'axios';
import FileUploadForm from './components/FileUploadForm';
import Table from 'react-bootstrap/Table';

const FileVersions = () => {
  const [fileVersions, setFileVersions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploadingError, setUploadingError] = useState('');

  useEffect(() => {
    const fetchFileVersions = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost:8001/api/file_versions/', {
          headers: {
            Authorization: `Token ${token}`, // Use Bearer token format
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

  const handleFileDownload = async (fileId, fileName) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`http://localhost:8001/api/file_versions/${fileId}/download`, {
        headers: {
          Authorization: `Token ${token}`, // Use Bearer token format
        },
        responseType: 'blob', // Ensure response is treated as a blob
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.target = '_blank'; // Open in a new tab/window
      link.setAttribute('download', fileName); // Set the download attribute to trigger the download
      document.body.appendChild(link);
      link.click();
    } catch (error) {
      console.error('Error downloading file:', error);
    }
  };

  return (
    <div>
      <div className='text-center'><h1>Welcome to Document Management</h1></div>
      <br></br>
      <br></br>
      <div className='text-center'> <FileUploadForm setUploadingError={setUploadingError}/></div>
      <br></br>
      {uploadingError&&<div className="text-danger text-center">{uploadingError}</div>}
      <br></br>
      <br></br>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <Table striped bordered hover>
          <thead>
            <tr>
              <th>File Name</th>
              <th>Versions</th>
            </tr>
          </thead>
          <tbody>
            {/* Group file versions by file name */}
            {Array.from(new Set(fileVersions.map((fileVersion) => fileVersion.file_name))).map((fileName, index) => (
              <tr key={index}>
                <td>{fileName}</td>
                <td>
                  {/* Display comma-separated version numbers with clickable links */}
                  {fileVersions
                    .filter((fileVersion) => fileVersion.file_name === fileName)
                    .map((fileVersion, index) => (
                      <a
                        key={index}
                        href="#"
                        onClick={(e) => {
                          e.preventDefault();
                          handleFileDownload(fileVersion.id, fileVersion.file_name); // Pass file name as well
                        }}
                      >
                        {fileVersion.version_number}
                      </a>
                    ))
                    .reduce((prev, curr) => [prev, ', ', curr])}
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}
    </div>
  );
};

export default FileVersions;
