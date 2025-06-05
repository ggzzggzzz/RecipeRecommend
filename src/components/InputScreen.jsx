import { styles } from '../styles/commonStyles';

export default function InputScreen({
  ingredients,
  setIngredients,
  input,
  setInput,
  setScreen,
}) {
  const addIngredient = (item) => {
    if (item && !ingredients.includes(item)) {
      setIngredients([...ingredients, item]);
    }
  }; 

  const removeIngredient = (item) => {
    setIngredients(ingredients.filter((i) => i !== item));
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <button style={styles.backBtn} onClick={() => setScreen('home')}>←</button>
        <span>식재료 입력</span>
      </div>
      <div style={{ display: 'flex', gap: 8 }}>
        <input
          style={styles.input}
          placeholder="텍스트 입력"
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button
          style={styles.photoBtn}
          onClick={() => setScreen('camera')}
        >
          사진 촬영
        </button>
      </div>
      <div style={styles.ingredientBox}>
        {ingredients.map((item) => (
          <div key={item} style={styles.ingredientItem}>
            {item}
            <button style={styles.removeBtn} onClick={() => removeIngredient(item)}>×</button>
          </div>
        ))}
      </div>
      <button
        style={styles.addBtn}
        onClick={() => {
          addIngredient(input.trim());
          setInput('');
        }}
      >
        추가
      </button>
    </div>
  );
}
