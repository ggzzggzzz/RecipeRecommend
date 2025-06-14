import { useState } from 'react';
import { styles } from '../styles/commonStyles';

export default function LoginScreen({ setScreen, setUserId , setNickname }) {
  const [loginId, setLoginId] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async () => {
    try {
      const response = await fetch('http://localhost:8000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
          user_id: loginId,
          password: password,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        alert(`${data.nickname}님, 환영합니다!`);
        setUserId(loginId);  // props로 받은 함수 호출!
        setNickname(data.nickname); // 닉네임 상태 설정
        setScreen('home');
      } else {
        setError(data.detail || '로그인 실패');
      }
    } catch (err) {
      setError('서버 연결 실패');
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <button style={styles.backBtn} onClick={() => setScreen('home')}>←</button>
        <span>로그인</span>
        <span></span>
      </div>

      <input
        style={styles.input}
        placeholder="아이디"
        value={loginId}
        onChange={(e) => setLoginId(e.target.value)}
      />
      <input
        style={styles.input}
        placeholder="비밀번호"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      {error && <p style={{ color: 'red' }}>{error}</p>}

      <button style={styles.button} onClick={handleLogin}>로그인</button>
      <p style={{ marginTop: '1rem' }}>
        계정이 없으신가요?{' '}
        <span
          style={{ color: 'blue', cursor: 'pointer' }}
          onClick={() => setScreen('signup')}
        >
          회원가입
        </span>
      </p>
    </div>
  );
}
