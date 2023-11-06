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

    const isURL = (str) => {
        const pattern = /^(https?:\/\/)?([\da-z.-]+)\.([a-z.]{2,6})([/\w .-]*)*\/?$/;
        return pattern.test(str);
      };

    const handleShorten = async () => {
      if (!isURL(longLink)) {
        alert('Please enter the correct URL');
        return;
      };

      try {
        const newShortLink = await ShortenerService.getShortLink(longLink);

        setShortLink(newShortLink);
        setLongLink(newShortLink);
        inputRef.current.value = newShortLink;
        setIsCopyButtonActive(true);

      } catch (error) {
        console.error('Error:', error);
        setShortLink('');
        setLongLink('');
        setIsCopyButtonActive(false);
      };
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

    const handleEnterKey = () => {
        if (longLink) {
            handleShorten();
        }
      };

    return (
      <div className="app-container">
          <div className="form-container">
              <InputField
                ref={inputRef}
                value={longLink}
                onChange={setLongLink}
                onEnter={handleEnterKey}
              />
              <ShortenButton onClick={handleShorten} />
              <CopyButton onClick={handleCopy} disabled={!isCopyButtonActive} />
          </div>
      </div>
        );
      };

  export default App;
