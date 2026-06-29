import { useState } from "react";
import FamilyBanner from "./FamilyBanner";
import ParentComponent from "./ParentComponent";
import ChildComponent from "./ChildComponent";
import "../App.css";

export default function App() {
  const [parentAssets, setParentAssets] = useState(500);
  const [childAssets, setChildAssets] = useState(0);

  function handleInherit() {
    alert("재산을 받았습니다!");
    setChildAssets(childAssets + parentAssets);
    setParentAssets(0);
  }

  return (
    <main className="app">
      <h1>useState 실습 — 가문의 재산</h1>
      <FamilyBanner familyName="React 가문" />
      <ParentComponent name="부모님" assets={parentAssets} />
      <ChildComponent
        name="자녀"
        assets={childAssets}
        onReceive={handleInherit}
      />
    </main>
  );
}

