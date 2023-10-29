import React, { useState, useRef } from 'react';
import InputField from "../../ui/InputField.tsx"
import ShortenButton from "../../ui/ShortenButton.tsx"
import CopyButton from "../../ui/CopyButton.tsx"
import './App.css';
import { ShortenerService } from '../../../services/shortener.service.js'

const App = () => {
    const [longLink, setLongLink] = useState('');
    const [shortLink, setShortLink] = useState('');
    const [isCopyButtonActive, setIsCopyButtonActive] = useState(false);

    const inputRef = useRef();

    const shortenLink = async (longLink) => {
        const shortLink = await ShortenerService.getShortLink(longLink)
        return shortLink
      };

    const handleShorten = async () => {
        const newShortLink = await shortenLink(longLink);
        setShortLink(newShortLink);
        setLongLink(newShortLink);
        inputRef.current.value = newShortLink;
        setIsCopyButtonActive(true);
      };

    const handleCopy = () => {
        navigator.clipboard.writeText(shortLink)
          .then(() => {
            setLongLink('');
            inputRef.current.value = '';
            setIsCopyButtonActive(false);
          })
          .catch((error) => {
            console.error('Error:', error);
          });
      };

      return (
        <div className="app-container">
            <div className="form-container">
                <InputField ref={inputRef} value={longLink} onChange={setLongLink} />
                <ShortenButton onClick={handleShorten} />
                <CopyButton onClick={handleCopy} disabled={!isCopyButtonActive} />
            </div>
        </div>
    );
  };

  export default App;
