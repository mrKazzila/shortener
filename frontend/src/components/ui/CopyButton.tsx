import React from 'react';

const CopyButton = ({ onClick, disabled }) => {
    return <button
      className="copy-button"
      onClick={onClick}
      disabled={disabled}
    >
      Copy
    </button>;
  };

export default CopyButton;
