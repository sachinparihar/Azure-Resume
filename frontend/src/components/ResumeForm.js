import React, { useState } from 'react';
import axios from 'axios';
import jsPDF from 'jspdf';
import fileSaver from 'file-saver';

const ResumeForm = () => {
  const [resumeData, setResumeData] = useState({
    name: '',
    skills: [],
    email: '',
    experience: '',
  });
  const [error, setError] = useState(null);
  const [downloadLink, setDownloadLink] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post('https://azure-resume-api.azurewebsites.net/api/GetResume', resumeData);
      if (response.status >= 200 && response.status < 300) {
        console.log('Resume created successfully!');
        const resumeDataJson = JSON.stringify(resumeData, null, 2);
        const pdf = new jsPDF();
        pdf.text(resumeDataJson, 10, 10);
        const pdfBlob = pdf.output('blob');
        const jsonBlob = new Blob([resumeDataJson], { type: 'application/json' });

        // Create download links for PDF and JSON files
        const pdfLink = URL.createObjectURL(pdfBlob);
        const jsonLink = URL.createObjectURL(jsonBlob);
        setDownloadLink({
          pdf: pdfLink,
          json: jsonLink,
        });
      } else {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      setError(error.message);
    }
  };

  const handleChange = (event) => {
    const { name, value } = event.target;
    setResumeData((prevData) => ({ ...prevData, [name]: value }));
  };

  const handleDownloadPdf = () => {
    fileSaver.saveAs(downloadLink.pdf, 'esume.pdf');
  };

  const handleDownloadJson = () => {
    fileSaver.saveAs(downloadLink.json, 'esume.json');
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Name:
        <input type="text" name="name" value={resumeData.name} onChange={handleChange} />
      </label>
      <br />
      <label>
        Skills:
        <input type="text" name="skills" value={resumeData.skills} onChange={handleChange} />
      </label>
      <br />
      <label>
        Email:
        <input type="email" name="email" value={resumeData.email} onChange={handleChange} />
      </label>
      <br />
      <label>
        Experience:
        <input type="text" name="experience" value={resumeData.experience} onChange={handleChange} />
      </label>
      <br />
      <button type="submit">Create Resume</button>
      {error && <div>Error: {error}</div>}
      {downloadLink && (
        <div className="download-buttons">
          <button className="download-pdf-button" onClick={handleDownloadPdf}>Download PDF</button>
          <button className="download-json-button" onClick={handleDownloadJson}>Download JSON</button>
        </div>
      )}
    </form>
  );
};

export default ResumeForm;