import { useEffect } from 'react';
import { testApiWrapper } from './lib/api.test';

const TestApi = () => {
  useEffect(() => {
    // Run the API wrapper test when component mounts
    testApiWrapper().catch(console.error);
  }, []);

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>API Wrapper Verification</h1>
      <p>Checking API wrapper functionality in mock mode...</p>
      <p>Check the browser console for detailed test results.</p>
      <div style={{ marginTop: '20px', color: 'gray' }}>
        <p><strong>Note:</strong> This test automatically verifies:</p>
        <ul>
          <li>Successful data retrieval from all endpoints</li>
          <li>Type safety and correct data structure</li>
          <li>Proper handling of mock vs live modes</li>
          <li>Correct configuration of base URL and headers</li>
        </ul>
      </div>
    </div>
  );
};

export default TestApi;
