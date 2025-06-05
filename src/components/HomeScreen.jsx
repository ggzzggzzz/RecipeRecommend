import { styles } from '../styles/commonStyles';

export default function HomeScreen({ setScreen }) {
  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <span></span>
        <span>홈</span>
        <span style={styles.menuIcon}>≡</span>
      </div>
      <button style={styles.button} onClick={() => setScreen('input')}>식재료 입력</button>
      <button style={styles.button} onClick={() => setScreen('recipe')}>추천 레시피</button>
    </div>
  );
}
