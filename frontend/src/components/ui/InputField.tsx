import React from 'react';

const InputField = ({ value, onChange }) => {
  return (
    <input
      type="text"
      value={value}
      onChange={e => onChange(e.target.value)}
      placeholder="Enter long url"
    />
  );
};

export default InputField;
