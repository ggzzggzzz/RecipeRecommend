import { useState } from 'react';
import { styles } from '../styles/commonStyles';

export default function HomeScreen({ setScreen , nickname }) {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <span></span>
        <span>홈</span>
        <span
          style={styles.menuIcon}
          onClick={() => setMenuOpen((prev) => !prev)}
        >
          ≡
        </span> 
      </div>

       {/* 환영 메시지 */}
      {nickname && (
        <div style={{ margin: '1rem 0', fontSize: '0.95em', color: '#555' }}>
          👋 {nickname}님, 환영합니다!
        </div>
      )}

      {/* 메뉴 버튼 */}
      {menuOpen && (
        <div style={{ marginBottom: '1rem' }}>
          <button style={styles.button} onClick={() => setScreen('login')}>로그인</button>
          <button style={styles.button} onClick={() => setScreen('signup')}>회원가입</button>
          <button style={styles.button} onClick={() => setScreen('mypage')}>마이페이지</button>
        </div>
      )}

      {/* 기본 버튼 */}
      <button style={styles.button} onClick={() => setScreen('input')}>식재료 입력</button>
      <button style={styles.button} onClick={() => setScreen('recipe')}>추천 레시피</button>
    </div>
  );
}
