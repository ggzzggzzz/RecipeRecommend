import { useState } from 'react';
import { styles } from '../styles/commonStyles';

export default function HomeScreen({ setScreen }) {
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

      {/* 메뉴 버튼 */}
      {menuOpen && (
        <div style={{ marginBottom: '1rem' }}>
          <button style={styles.button} onClick={() => alert('로그인 페이지 이동')}>로그인</button>
          <button style={styles.button} onClick={() => alert('회원가입 페이지 이동')}>회원가입</button>
          <button style={styles.button} onClick={() => setScreen('mypage')}>마이페이지</button>
        </div>
      )}

      {/* 기본 버튼 */}
      <button style={styles.button} onClick={() => setScreen('input')}>식재료 입력</button>
      <button style={styles.button} onClick={() => setScreen('recipe')}>추천 레시피</button>
    </div>
  );
}
