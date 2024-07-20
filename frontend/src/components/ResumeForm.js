import React, { useState } from 'react';
import axios from 'axios';
import jsPDF from 'jspdf';
import fileSaver from 'file-saver';

const ResumeForm = () => {
  const [resumeData, setResumeData] = useState({
    basics: {
      name: '',
      label: '',
      email: '',
      website: '',
      summary: '',
      location: {
        city: '',
        countryCode: '',
        region: ''
      },
      profiles: []
    },
    work: [],
    education: [],
    awards: [],
    skills: [],
    interests: []
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
    setResumeData((prevData) => {
      if (name === 'name') {
        prevData.basics.name = value;
      } else if (name === 'label') {
        prevData.basics.label = value;
      } else if (name === 'email') {
        prevData.basics.email = value;
      } else if (name === 'website') {
        prevData.basics.website = value;
      } else if (name === 'ummary') {
        prevData.basics.summary = value;
      } else if (name === 'city') {
        prevData.basics.location.city = value;
      } else if (name === 'countryCode') {
        prevData.basics.location.countryCode = value;
      } else if (name === 'egion') {
        prevData.basics.location.region = value;
      } else if (name.startsWith('profile-')) {
        const profileIndex = parseInt(name.split('-')[1]);
        prevData.basics.profiles[profileIndex] = value;
      } else if (name.startsWith('work-')) {
        const workIndex = parseInt(name.split('-')[1]);
        prevData.work[workIndex] = value;
      } else if (name.startsWith('education-')) {
        const educationIndex = parseInt(name.split('-')[1]);
        prevData.education[educationIndex] = value;
      } else if (name.startsWith('award-')) {
        const awardIndex = parseInt(name.split('-')[1]);
        prevData.awards[awardIndex] = value;
      } else if (name.startsWith('skill-')) {
        const skillIndex = parseInt(name.split('-')[1]);
        prevData.skills[skillIndex] = value;
      } else if (name.startsWith('interest-')) {
        const interestIndex = parseInt(name.split('-')[1]);
        prevData.interests[interestIndex] = value;
      }
      return prevData;
    });
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
        <input type="text" name="name" value={resumeData.basics.name} onChange={handleChange} />
      </label>
      <br />
      <label>
        Label:
        <input type="text" name="label" value={resumeData.basics.label} onChange={handleChange} />
      </label>
      <br />
      <label>
        Email:
        <input type="email" name="email" value={resumeData.basics.email} onChange={handleChange} />
      </label>
      <br />
      <label>
        Website:
        <input type="text" name="website" value={resumeData.basics.website} onChange={handleChange} />
      </label>
      <br />
      <label>
        Summary:
        <textarea name="summary" value={resumeData.basics.summary} onChange={handleChange} />
      </label>
      <br />
      <label>
        City:
        <input type="text" name="city" value={resumeData.basics.location.city} onChange={handleChange} />
      </label>
      <br />
      <label>
        Country Code:
        <input type="text" name="countryCode" value={resumeData.basics.location.countryCode} onChange={handleChange} />
      </label>
      <br />
      <label>
        Region:
        <input type="text" name="region" value={resumeData.basics.location.region} onChange={handleChange} />
      </label>
      <br />
      <h2>Profiles</h2>
      {resumeData.basics.profiles.map((profile, index) => (
        <label key={index}>
          Profile {index + 1}:
          <input type="text" name={`profile-${index}`} value={profile} onChange={handleChange} />
        </label>
      ))}
      <br />
      <h2>Work Experience</h2>
      {resumeData.work.map((work, index) => (
        <label key={index}>
          Work {index + 1}:
          <input type="text" name={`work-${index}`} value={work} onChange={handleChange} />
        </label>
      ))}
      <br />
      <h2>Education</h2>
      {resumeData.education.map((education, index) => (
        <label key={index}>
          Education {index + 1}:
          <input type="text" name={`education-${index}`} value={education} onChange={handleChange} />
        </label>
      ))}
      <br />
      <h2>Awards</h2>
      {resumeData.awards.map((award, index) => (
        <label key={index}>
          Award {index + 1}:
          <input type="text" name={`award-${index}`} value={award} onChange={handleChange} />
        </label>
      ))}
      <br />
      <h2>Skills</h2>
      {resumeData.skills.map((skill, index) => (
        <label key={index}>
          Skill {index + 1}:
          <input type="text" name={`skill-${index}`} value={skill} onChange={handleChange} />
        </label>
      ))}
      <br />
      <h2>Interests</h2>
      {resumeData.interests.map((interest, index) => (
        <label key={index}>
          Interest {index + 1}:
          <input type="text" name={`interest-${index}`} value={interest} onChange={handleChange} />
        </label>
      ))}
      <br />
      <button type="submit">Create Resume</button>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {downloadLink && (
        <div>
          <button onClick={handleDownloadPdf}>Download PDF</button>
          <button onClick={handleDownloadJson}>Download JSON</button>
        </div>
      )}
    </form>
  );
};

export default ResumeForm;