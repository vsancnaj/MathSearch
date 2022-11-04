import React from 'react';

import UploadPDFToS3WithNativeSdk from '../UploadPDFToS3WithNativeSdk.js';
import LaTeXInput from '../LaTeXInput.js';

import '../../App.css';
import './Home.css'

function Home() {
  return (
    <>
      <div className="home-container">
        <div className="home-content">
          <h1 className="title">MathSearch</h1>
          <LaTeXInput/>
          <UploadPDFToS3WithNativeSdk />
        </div>
      </div>
    </>
  );
}

export default Home;
