import React, { useCallback } from 'react';
import { UploadCloud, FileAudio } from 'lucide-react';

const AudioUploader = ({ file, setFile, label, disabled }) => {
    const handleFileChange = (e) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
        }
    };

    return (
        <div className="glass-pane upload-zone">
            <h3>{label}</h3>
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '10px' }}>
                {file ? (
                    <>
                        <FileAudio size={48} color="var(--color-primary-light)" />
                        <span>{file.name}</span>
                        <button className="btn" onClick={() => setFile(null)} disabled={disabled}>Change File</button>
                    </>
                ) : (
                    <>
                        <UploadCloud size={48} color="gray" />
                        <input
                            type="file"
                            accept="audio/*"
                            onChange={handleFileChange}
                            disabled={disabled}
                            id={`file-upload-${label}`}
                            style={{ display: 'none' }}
                        />
                        <label htmlFor={`file-upload-${label}`} className="btn" style={{ cursor: 'pointer' }}>
                            Select Audio
                        </label>
                    </>
                )}
            </div>
        </div>
    );
};

export default AudioUploader;
