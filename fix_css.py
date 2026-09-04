import re

with open('static/css/style.css', 'rb') as f:
    content_bytes = f.read()

# The file might contain null bytes from UTF-16, let's just decode ignoring errors
content_str = content_bytes.decode('utf-8', errors='ignore')

# The corrupted part starts after the last valid CSS rule which we know was in the file originally.
# Or we can just find where the weird spaces start.
# Let's search for "/* Like Button */" or " / *   L i k e"
# The string might look like "\x00\n\x00/\x00*\x00" if it was UTF-16LE.

# An easier way is to just read the file, and since the original file was ~15500 bytes, we can just truncate.
# Wait, I know the corrupted part was appended at the very end. Let's just find the last valid `}` of the `@media` query or similar.

# Instead of truncating by guessing, let's use a regex to find the `ÿþ` (BOM) or null bytes and strip everything after.
# Wait, let's just find the first null byte, and strip from there.
idx = content_bytes.find(b'\x00')
if idx != -1:
    # There are null bytes! It means the appended UTF-16 starts somewhere.
    # Let's find the `\xff\xfe` BOM which powershell uses.
    bom_idx = content_bytes.find(b'\xff\xfe')
    if bom_idx != -1:
        content_bytes = content_bytes[:bom_idx]
    else:
        # Just find the first null byte and go back to the previous newline
        content_bytes = content_bytes[:idx]

clean_content = content_bytes.decode('utf-8', errors='ignore')

# Now append the correct CSS
like_css = """

/* Like Button */
.like-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    background: rgba(255, 255, 255, 0.8);
    border: none;
    border-radius: 50%;
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    z-index: 10;
}

[data-theme="dark"] .like-btn {
    background: rgba(0, 0, 0, 0.5);
}

.like-btn:hover {
    transform: scale(1.1);
}

.like-btn svg {
    color: #9ca3af;
    fill: none;
    transition: all 0.3s ease;
}

.like-btn.liked svg {
    color: #ef4444;
    fill: #ef4444;
}

.like-btn.liked {
    animation: heartBeat 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

@keyframes heartBeat {
    0% { transform: scale(1); }
    50% { transform: scale(1.3); }
    100% { transform: scale(1); }
}
"""

with open('static/css/style.css', 'w', encoding='utf-8') as f:
    f.write(clean_content + like_css)

print("Cleaned and fixed style.css!")
