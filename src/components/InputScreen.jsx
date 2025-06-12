import { styles } from '../styles/commonStyles';
import { useEffect } from 'react';

export default function InputScreen({
  ingredients,
  setIngredients,
  input,
  setInput,
  setScreen,
   userId // ← 추가
}) {
  
  useEffect(() => {
  const fetchIngredients = async () => {
    try {
      const res = await fetch(`http://localhost:8000/user-ingredients?user_id=${userId}`);
      const data = await res.json();
      if (res.ok) {
        setIngredients(data.ingredients || []);
      } else {
        console.error(data.detail || '식재료 불러오기 실패');
      }
    } catch (err) {
      console.error('보유 식재료 조회 실패:', err);
    }
  };

  if (userId) {
    fetchIngredients();
  }
}, [userId]);



  const addIngredient = async (item) => {
  const trimmedItem = item.trim();
  if (!trimmedItem || ingredients.includes(trimmedItem)) return;

  try {
    const res = await fetch('http://localhost:8000/add-ingredient', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        user_id: userId,
        name: trimmedItem,
      }),
    });

    const data = await res.json();

    if (!res.ok) {
      alert(data.detail);  // 예: '등록되지 않은 식재료입니다'
    } else {
      // ✅ 성공 시에만 화면에 추가
      setIngredients([...ingredients, trimmedItem]);
      console.log(data.message);
    }
  } catch (err) {
    console.error('식재료 등록 실패:', err);
  }
};



  const removeIngredient = async (item) => {
  setIngredients(ingredients.filter((i) => i !== item));

  try {
    const res = await fetch('http://localhost:8000/remove-ingredient', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        user_id: userId,
        name: item,
      }),
    });

    const data = await res.json();

    if (!res.ok) {
      alert(data.detail);
    } else {
      console.log(data.message);
    }
  } catch (err) {
    console.error('식재료 삭제 실패:', err);
  }
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
        addIngredient(input);
        setInput('');
      }}

      >
        추가
      </button>
    </div>
  );
}
