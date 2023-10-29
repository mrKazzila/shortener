import React, { forwardRef } from 'react';


const InputField = forwardRef(({ value, onChange, onEnter }, ref) => {
    const handleKeyDown = (e) => {
      if (e.key === 'Enter') {
        onEnter();
      }
    };
    return (
        <input
            type="text"
            className="input-field"
            value={value}
            onChange={(e) => onChange(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Enter long url"
            ref={ref}
        />
    );
});

export default InputField;
