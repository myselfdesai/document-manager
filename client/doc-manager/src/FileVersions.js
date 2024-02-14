import React, { useState, useEffect } from 'react';
import axios from 'axios';
import FileUploadForm from './components/FileUploadForm';
import Table from 'react-bootstrap/Table';


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
      <div className='text-center'><h1>Welcome to Document Management</h1></div>
      <br></br>
      <br></br>
      <div className='text-center'> <FileUploadForm onFileUploaded={handleFileUploaded} /></div>
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
      {fileVersions.map((fileVersion) => (
        <tr key={fileVersion.id}>
          <td>{fileVersion.file_name}</td>
          <td>{fileVersion.version_number}</td>
        </tr>
        ))}
        </tbody>
      </Table>
        
      )}
    </div>
  );
};

export default FileVersions;