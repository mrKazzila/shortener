import React, { useState } from 'react';
import InputField from "../../ui/InputField.tsx"
import ShortenButton from "../../ui/ShortenButton.tsx"
import CopyButton from "../../ui/CopyButton.tsx"
import './App.css';
import { ShortenerService } from '../../../services/shortener.service.js'

const App = () => {
    const [longLink, setLongLink] = useState('');
    const [shortLink, setShortLink] = useState('');

    const shortenLink = async (longLink) => {
        const shortLink = await ShortenerService.getShortLink(longLink)
        return shortLink
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
        <div className="app-container">
            <div className="form-container">
                <InputField value={longLink} onChange={setLongLink} />
                <ShortenButton onClick={handleShorten} />
            </div>
            {shortLink && <div className="short-link">{shortLink}</div>}
            {shortLink && <CopyButton onClick={handleCopy} />}
        </div>
    );
  };

  export default App;
