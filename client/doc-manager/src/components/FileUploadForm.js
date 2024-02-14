import React, { useState } from 'react';
import axios from 'axios';

const FileUploadForm = (props) => {
  const { setUploadingError } = props;
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleFileUpload = async () => {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const token = localStorage.getItem('token');
      const response = await axios.post('http://localhost:8001/api/file_upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: `Token ${token}`,
        },
      }).then(
        (response) => {
          window.location.reload();
        }
      ).catch(()=>{
        setUploadingError('File already exists');
      });
      
      
    } catch (error) {
      setUploadingError('File already exists');
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleFileUpload}>Upload</button>
    </div>
  );
};

export default FileUploadForm;