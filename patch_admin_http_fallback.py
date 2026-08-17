from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

old = '''    async function sha256(text) {
      const bytes = new TextEncoder().encode(text);
      const hashBuffer = await crypto.subtle.digest('SHA-256', bytes);
      return Array.from(new Uint8Array(hashBuffer)).map(b => b.toString(16).padStart(2, '0')).join('');
    }
'''

new = r'''    function sha256Fallback(ascii) {
      function rightRotate(value, amount) {
        return (value >>> amount) | (value << (32 - amount));
      }

      const mathPow = Math.pow;
      const maxWord = mathPow(2, 32);
      const words = [];
      const asciiBitLength = ascii.length * 8;
      const hash = [];
      const k = [];
      const isComposite = {};
      let primeCounter = 0;
      let i, j;

      for (let candidate = 2; primeCounter < 64; candidate++) {
        if (!isComposite[candidate]) {
          for (i = 0; i < 313; i += candidate) isComposite[i] = candidate;
          hash[primeCounter] = (mathPow(candidate, .5) * maxWord) | 0;
          k[primeCounter++] = (mathPow(candidate, 1 / 3) * maxWord) | 0;
        }
      }

      ascii += '\x80';
      while (ascii.length % 64 - 56) ascii += '\x00';

      for (i = 0; i < ascii.length; i++) {
        j = ascii.charCodeAt(i);
        if (j >> 8) throw new Error('Fallback SHA-256 only supports ASCII admin codes.');
        words[i >> 2] |= j << ((3 - i) % 4) * 8;
      }

      words[words.length] = (asciiBitLength / maxWord) | 0;
      words[words.length] = asciiBitLength;

      let currentHash = hash.slice(0, 8);
      for (j = 0; j < words.length;) {
        const w = words.slice(j, j += 16);
        const oldHash = currentHash.slice(0);

        for (i = 0; i < 64; i++) {
          const w15 = w[i - 15];
          const w2 = w[i - 2];
          const a = currentHash[0];
          const e = currentHash[4];
          const temp1 = currentHash[7]
            + (rightRotate(e, 6) ^ rightRotate(e, 11) ^ rightRotate(e, 25))
            + ((e & currentHash[5]) ^ ((~e) & currentHash[6]))
            + k[i]
            + (w[i] = i < 16 ? w[i] : (
              w[i - 16]
              + (rightRotate(w15, 7) ^ rightRotate(w15, 18) ^ (w15 >>> 3))
              + w[i - 7]
              + (rightRotate(w2, 17) ^ rightRotate(w2, 19) ^ (w2 >>> 10))
            ) | 0);
          const temp2 = (rightRotate(a, 2) ^ rightRotate(a, 13) ^ rightRotate(a, 22))
            + ((a & currentHash[1]) ^ (a & currentHash[2]) ^ (currentHash[1] & currentHash[2]));

          currentHash = [(temp1 + temp2) | 0].concat(currentHash);
          currentHash[4] = (currentHash[4] + temp1) | 0;
          currentHash.pop();
        }

        for (i = 0; i < 8; i++) currentHash[i] = (currentHash[i] + oldHash[i]) | 0;
      }

      let result = '';
      for (i = 0; i < 8; i++) {
        for (j = 3; j + 1; j--) {
          const b = (currentHash[i] >> (j * 8)) & 255;
          result += (b < 16 ? '0' : '') + b.toString(16);
        }
      }
      return result;
    }

    async function sha256(text) {
      if (globalThis.crypto?.subtle && globalThis.TextEncoder) {
        const bytes = new TextEncoder().encode(text);
        const hashBuffer = await crypto.subtle.digest('SHA-256', bytes);
        return Array.from(new Uint8Array(hashBuffer)).map(b => b.toString(16).padStart(2, '0')).join('');
      }
      return sha256Fallback(String(text));
    }
'''

if old not in text:
    raise SystemExit('sha256 function anchor not found')
text = text.replace(old, new, 1)

old_submit = '''    async function submitAdminCode() {
      const enteredHash = await sha256(adminCodeInput.value);
      if (enteredHash === CONFIG.adminCodeHash) {
        state.adminCode = adminCodeInput.value;
        saveAdminCodeSession(state.adminCode);
        setAdminMode(true);
        closeAdminModal();
        syncAllLocalOverridesToCloud();
      } else {
        adminError.textContent = '관리자 코드가 올바르지 않습니다.';
        adminCodeInput.select();
      }
    }
'''

new_submit = '''    async function submitAdminCode() {
      try {
        const enteredHash = await sha256(adminCodeInput.value);
        if (enteredHash === CONFIG.adminCodeHash) {
          state.adminCode = adminCodeInput.value;
          saveAdminCodeSession(state.adminCode);
          setAdminMode(true);
          closeAdminModal();
          syncAllLocalOverridesToCloud();
        } else {
          adminError.textContent = '관리자 코드가 올바르지 않습니다.';
          adminCodeInput.select();
        }
      } catch (err) {
        console.error('관리자 인증 처리 실패', err);
        adminError.textContent = '관리자 인증 처리 중 오류가 발생했습니다. 새로고침 후 다시 시도해 주세요.';
      }
    }
'''

if old_submit not in text:
    raise SystemExit('submitAdminCode anchor not found')
text = text.replace(old_submit, new_submit, 1)

p.write_text(text, encoding='utf-8')
