import React from 'react';

const ShortenButton = ({ onClick }) => {
  return <button className="shorten-button" onClick={onClick}>Cut url</button>;
};

export default ShortenButton;
