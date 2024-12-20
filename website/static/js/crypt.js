async function generateKey(data, salt) {
    const encData = new TextEncoder().encode(data.map(d => `${d}>>`).join(''));

    const keyMaterial = await crypto.subtle.importKey(
        'raw',                  
        encData,                    
        { name: 'PBKDF2' },        
        false,                      
        ['deriveKey']               
    );

    return crypto.subtle.deriveKey(
        {
            name: 'PBKDF2',
            salt: salt,               
            iterations: 100000,       
            hash: 'SHA-256'    
        },
        keyMaterial,
        { name: 'AES-CFB', length: 256 },
        true,
        ['encrypt', 'decrypt']     
    );
}

async function exportKeyToString(key) {
    const rawKey = await crypto.subtle.exportKey("raw", key);
    const rawKeyArray = new Uint8Array(rawKey);
    return btoa(String.fromCharCode(...rawKeyArray));
}

async function importKeyFromString(keyString) {
    const rawKeyArray = Uint8Array.from(atob(keyString), c => c.charCodeAt(0));

    return await crypto.subtle.importKey(
        "raw",
        rawKeyArray.buffer,
        { name: "AES-CFB" },
        true,
        ["encrypt", "decrypt"]
    );
}

async function encryptData(key, plainText) {
    const iv = crypto.getRandomValues(new Uint8Array(16));
    const encodedText = new TextEncoder().encode(plainText);

    const ciphertext = await crypto.subtle.encrypt(
        { name: 'AES-CFB', iv: iv }, 
        key,              
        encodedText         
    );
    
    const combined = new Uint8Array(iv.byteLength + ciphertext.byteLength);
    combined.set(iv);
    combined.set(new Uint8Array(ciphertext), iv.byteLength);
    return btoa(String.fromCharCode(...combined));
}

async function decryptData(key, encodedCiphertext) {
    const combined = Uint8Array.from(atob(encodedCiphertext), c => c.charCodeAt(0));

    const iv = combined.slice(0, 16); 
    const ciphertext = combined.slice(16); 
    
    const plainTextBuffer = await crypto.subtle.decrypt(
        { name: 'AES-CFB', iv: iv }, 
        key,                        
        ciphertext     
    );

    return new TextDecoder().decode(plainTextBuffer);
}