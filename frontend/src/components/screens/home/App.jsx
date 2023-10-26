import React, { useState } from 'react';
import InputField from "../../ui/InputField"
import ShortenButton from "../../ui/ShortenButton"
import CopyButton from "../../ui/CopyButton"

const App = () => {
    const [longLink, setLongLink] = useState('');
    const [shortLink, setShortLink] = useState('');

    const shortenLink = async (longLink) => {
        try {
          const response = await fetch('http://0.0.0.0:8000/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ target_url: longLink }),
          });

          const data = await response.json();
          const shortLink = data.url;

          return shortLink;
        } catch (error) {
          console.error('Error', error);
        }
      };

    const handleShorten = async () => {
        const newShortLink = await shortenLink(longLink);
        setShortLink(newShortLink);
      };

    const handleCopy = () => {
        navigator.clipboard.writeText(shortLink)
          .then(() => {
            alert('Copy to clipboard');
          })
          .catch((error) => {
            console.error('Error:', error);
          });
      };

    return (
      <div style={{ textAlign: 'center', marginTop: '50px' }}>
        <div style={{ display: 'inline-block' }}>
          <InputField value={longLink} onChange={setLongLink} />
          <ShortenButton onClick={handleShorten} />
        </div>
        {shortLink && <div style={{ marginTop: '20px' }}>{shortLink}</div>}
        {shortLink && <CopyButton onClick={handleCopy} />}
      </div>
    );
  };

  export default App;
