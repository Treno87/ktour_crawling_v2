"""
Slack 알림 전송 모듈
"""
import requests
import json
import os


class SlackNotifier:
    """슬랙 알림 전송 클래스"""

    def __init__(self, webhook_url=None):
        self.webhook_url = webhook_url or os.getenv('SLACK_WEBHOOK_URL')

    def send_message(self, message: str) -> bool:
        """
        슬랙 메시지 전송

        Args:
            message: 전송할 메시지 내용

        Returns:
            bool: 전송 성공 여부
        """
        if not self.webhook_url:
            print("[WARNING] Slack Webhook URL이 설정되지 않아 알림을 보낼 수 없습니다.")
            return False

        try:
            payload = {'text': message}
            response = requests.post(
                self.webhook_url,
                data=json.dumps(payload),
                headers={'Content-Type': 'application/json'}
            )

            if response.status_code == 200:
                print("[OK] 슬랙 알림 전송 성공")
                return True
            else:
                print(f"[ERROR] 슬랙 알림 전송 실패: HTTP {response.status_code}")
                return False

        except Exception as e:
            print(f"[ERROR] 슬랙 알림 전송 중 오류 발생: {e}")
            return False

    def _append_reservation_block(
        self,
        message: list,
        res: dict,
        idx: int,
        include_date: bool,
        is_new_section: bool
    ):
        """예약 정보 블록을 메시지에 추가"""
        # 고객명
        name = res.get('고객명', '고객')
        team = res.get('팀', '')
        if team and team != 'TEAM 1':
            name_line = f"*{idx}. {name}* ({team})"
        else:
            name_line = f"*{idx}. {name}*"
        message.append(name_line)

        # 시간, 채널, 인원
        time_str = res.get('예약시간', '시간미정')
        channel = res.get('채널', '-')
        people = res.get('인원구분', '-')

        # 날짜 포함 여부
        if include_date:
            date = res.get('날짜', '')
            message.append(f"📅 {date} | 🕐 {time_str} | 🧭 {channel} | 👤 {people}")
        else:
            message.append(f"🕐 {time_str} | 🧭 {channel} | 👤 {people}")

        # 서비스 및 가격
        product = res.get('예약상품', '-')
        price = self._parse_price(res.get('금액', '0'))

        if is_new_section:
            message.append(f"✂️ {product}")
            message.append(f"💰 {price:,}원")
            message.append("")  # 빈 줄
        else:
            message.append(f"✂️ {product} | 💰 {price:,}원\n")

    def _parse_price(self, price_str: str) -> int:
        """가격 문자열을 정수로 변환"""
        if isinstance(price_str, (int, float)):
            return int(price_str)
        try:
            return int(price_str.replace(',', ''))
        except (ValueError, AttributeError):
            return 0

    def _calculate_total_price(self, reservations: list[dict]) -> int:
        """전체 예약의 총 매출 계산"""
        return sum(self._parse_price(res.get('금액', '0')) for res in reservations)

    def format_daily_summary_message(
        self,
        today_reservations: list[dict],
        new_reservations: list[dict],
        today_date: str,
        notify_everyone: bool = False,
        sheet_url: str = None
    ) -> str:
        """
        당일 예약현황과 새로 추가된 예약을 구분하여 메시지 생성

        Args:
            today_reservations: 당일 예약 리스트
            new_reservations: 새로 추가된 예약 리스트 (모든 날짜 포함)
            today_date: 오늘 날짜 (예: "2026-01-18")
            notify_everyone: @channel 알림 포함 여부
            sheet_url: 구글 시트 URL (선택)

        Returns:
            str: 포맷팅된 메시지
        """
        message = []

        # @channel 알림
        if notify_everyone:
            message.append("<!channel>")

        # ===== 당일 예약현황 섹션 =====
        message.append(f"📅 *[{today_date}] 당일 예약현황*")
        message.append("━━━━━━━━━━━━━━━━━━")

        if today_reservations:
            idx = 1
            for res in today_reservations:
                self._append_reservation_block(
                    message, res, idx, include_date=False, is_new_section=False
                )
                idx += 1

            # 당일 매출
            today_total = self._calculate_total_price(today_reservations)
            message.append(f"💵 당일 예상 매출: *{today_total:,}원* ({len(today_reservations)}건)")
        else:
            message.append("예약이 없습니다.\n")

        # ===== 새로 추가된 예약 섹션 =====
        message.append("\n🆕 *[새로 추가된 예약]*")
        message.append("━━━━━━━━━━━━━━━━━━")

        if new_reservations:
            idx = 1
            for res in new_reservations:
                self._append_reservation_block(
                    message, res, idx, include_date=True, is_new_section=True
                )
                idx += 1

            # 새 예약 매출
            new_total = self._calculate_total_price(new_reservations)
            message.append("━━━━━━━━━━━━━━━━━━")
            message.append(f"💰 새 예약 매출: *{new_total:,}원* ({len(new_reservations)}건)")
        else:
            message.append("새로 추가된 예약이 없습니다.")

        # 시트 바로가기
        if sheet_url:
            message.append(f"\n🔗 <{sheet_url}|시트 바로가기>")

        return "\n".join(message)
