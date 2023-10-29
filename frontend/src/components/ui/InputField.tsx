import React, { forwardRef } from 'react';

const InputField = forwardRef(({ value, onChange }, ref) => {
    return (
        <input
            type="text"
            className="input-field"
            value={value}
            onChange={(e) => onChange(e.target.value)}
            placeholder="Enter long url"
            ref={ref}
        />
    );
});

export default InputField;
