# -*- coding: utf-8 -*-
"""
아이템 분배 계산기 (Colab용, 남은 아이템 자동 재분배 포함)
"""

from IPython.display import display
import ipywidgets as widgets

class ItemDistributor:
    """아이템 분배 계산 클래스"""

    def __init__(self, total_items, total_people, min_items, special_people, bonus_items):
        self.n = total_items
        self.c = total_people
        self.m = min_items
        self.a = special_people
        self.b = bonus_items
        self._validate()

    def _validate(self):
        if self.a > self.c:
            raise ValueError(f"❌ 특별 대상({self.a}명)이 전체 인원({self.c}명)보다 많을 수 없습니다.")
        if any(x < 0 for x in [self.n, self.c, self.m, self.a, self.b]):
            raise ValueError("❌ 모든 값은 0 이상이어야 합니다.")
        if self.c == 0:
            raise ValueError("❌ 전체 인원은 1명 이상이어야 합니다.")

    def calculate_minimum_required(self):
        return (self.c * self.m) + (self.a * self.b)

    def is_distributable(self):
        return self.n >= self.calculate_minimum_required()

    def calculate_remaining(self):
        return max(0, self.n - self.calculate_minimum_required())

    def calculate_shortage(self):
        return max(0, self.calculate_minimum_required() - self.n)

    def get_distribution(self):
        result = {
            "입력값": {
                "총_아이템": self.n,
                "전체_인원": self.c,
                "최소_개수": self.m,
                "특별_대상": self.a,
                "추가_개수": self.b
            },
            "최소_필요_아이템": self.calculate_minimum_required(),
            "분배_가능": self.is_distributable()
        }

        if not self.is_distributable():
            result["부족한_아이템"] = self.calculate_shortage()
            result["메시지"] = f"아이템이 {self.calculate_shortage()}개 부족합니다."
            return result

        # 기본 분배
        special_per_person = self.m + self.b
        normal_per_person = self.m
        leftover = self.calculate_remaining()

        # 🎯 남은 아이템 자동 분배 로직
        total_distributed = (self.a * special_per_person) + ((self.c - self.a) * normal_per_person)
        special_extra = 0
        normal_extra = 0

        while leftover >= self.c:  # 전체 인원에게 한 바퀴씩 돌릴 수 있을 때
            special_per_person += 1
            normal_per_person += 1
            leftover -= self.c
            special_extra += 1
            normal_extra += 1

        # 남은 아이템이 전체 인원보다 적을 경우
        if leftover > 0:
            if leftover <= self.a:
                # 특별 인원에게만 모두 줌
                special_per_person += leftover // self.a
                leftover = leftover % self.a  # ✅ 수정: 나머지 보존
            else:
                # 특별 인원에게 우선 지급 후 남으면 일반 인원에게
                give_special = self.a
                special_per_person += 1
                leftover -= give_special
                if leftover > 0:
                    # 남은 건 일반 인원에게
                    normal_per_person += leftover // (self.c - self.a)
                    leftover = leftover % (self.c - self.a)  # ✅ 수정: 나머지 보존

        result["분배_결과"] = {
            "특별_대상": {
                "인원": self.a,
                "인당_개수": special_per_person,
                "총_개수": self.a * special_per_person
            },
            "일반_대상": {
                "인원": self.c - self.a,
                "인당_개수": normal_per_person,
                "총_개수": (self.c - self.a) * normal_per_person
            },
        }
        result["최종_남은_아이템"] = leftover
        return result

    def print_report(self):
        """결과를 보기 좋게 출력"""
        result = self.get_distribution()
        print("="*65)
        print("🎯 아이템 분배 결과")
        print("="*65)
        print(f"총 아이템: {self.n}개")
        print(f"전체 인원: {self.c}명 (특별 {self.a}명 포함)")
        print(f"최소 보장 개수: {self.m}개, 특별 인원 추가 개수: {self.b}개")
        print("-"*65)
        print(f"최소 필요 아이템: {result['최소_필요_아이템']}개")
        print(f"분배 가능 여부: {'✅ 가능' if result['분배_가능'] else '❌ 불가능'}")
        print("-"*65)

        if result["분배_가능"]:
            dist = result["분배_결과"]
            print(f"[최종 분배]")
            print(f" • 일반 인원 {dist['일반_대상']['인원']}명 → 각 {dist['일반_대상']['인당_개수']}개 "
                  f"(총 {dist['일반_대상']['총_개수']}개)")
            print(" ")
            print(f" • 특별 인원 {dist['특별_대상']['인원']}명 → 각 {dist['특별_대상']['인당_개수']}개 "
                  f"(총 {dist['특별_대상']['총_개수']}개)")


            leftover = result["최종_남은_아이템"]
            print("\n[남은 아이템]")
            if leftover > 0:
                print(f" • 최종 남은 아이템 수 : {leftover}개 (모두 분배 후 남은 수량)")
            else:
                print(" • 남은 아이템 없음 (모두 분배 완료)")
        else:
            print(f"[부족 상황]")
            print(f" • 부족한 아이템: {result['부족한_아이템']}개")
            print(f" • {result['메시지']}")

        print("="*65)


# 🔹 Colab용 입력 UI 구성
n_input = widgets.IntText(value=0, description="총 아이템 수 :")
c_input = widgets.IntText(value=0, description="전체 인원 수 :")
m_input = widgets.IntText(value=1, description="최소 지급 수 :")
a_input = widgets.IntText(value=0, description="공무원 인원 :")
b_input = widgets.IntText(value=0, description="공무원 지급:")
run_button = widgets.Button(description="💡 계산 실행", button_style='success')

output = widgets.Output()

def on_run_clicked(_):
    output.clear_output()
    with output:
        try:
            dist = ItemDistributor(
                total_items=n_input.value,
                total_people=c_input.value,
                min_items=m_input.value,
                special_people=a_input.value,
                bonus_items=b_input.value
            )
            dist.print_report()
        except ValueError as e:
            print(e)

run_button.on_click(on_run_clicked)

# UI 표시
display(widgets.VBox([
    widgets.HTML("<h3>🎲 아이템 분배 계산기</h3>"),
    n_input, c_input, m_input, a_input, b_input,
    run_button,
    output
]))
