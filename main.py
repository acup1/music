import flet as ft
import asyncio,threading


playback=False
duration=0
current_position=0
current_position_text_value="00:00"
current_position_text_inverted_mode=0

def main(page: ft.Page):
    
    def upadate_controls(_):
        current_position=audio.get_current_position()
        duration=audio.get_duration()

        seek_sldr.value=current_position
        seek_sldr.max=duration

        if current_position_text_inverted_mode:
            current_position=duration-current_position
            current_position_text_value=f"-{('00'+str(current_position//1000//60))[-2:]}:{('00'+str(current_position//1000%60))[-2:]}"
        else:
            current_position_text_value=f"{('00'+str(current_position//1000//60))[-2:]}:{('00'+str(current_position//1000%60))[-2:]}"
        current_position_text.text=current_position_text_value

        page.update()

    def invert_current_position_text(_):
        global current_position_text_inverted_mode,duration,current_position
        current_position_text_inverted_mode=1-current_position_text_inverted_mode

    def playbtn_clk(_):
        global playback
        if playback:
            playback=False
            audio.pause()
            playbtn.icon=ft.icons.PLAY_CIRCLE
        else:
            playback=True
            audio.resume()
            playbtn.icon=ft.icons.PAUSE_CIRCLE
        page.update()
    
    def seek_sldr_change(_):
        audio.seek(int(seek_sldr.value))
        audio.update()

    def volume_sldr_change(_):
        audio.volume=volume_sldr.value
        audio.update()
        
    page=page
    audio = ft.Audio(
        src="https://luan.xyz/files/audio/ambient_c_motion.mp3",
        autoplay=False,
        on_state_changed=upadate_controls,
        on_position_changed=upadate_controls,
    )

    playbtn=ft.IconButton(
        icon=ft.icons.PLAY_CIRCLE,
        on_click=playbtn_clk,
        col=1
    )

    seek_sldr=ft.Slider(
        min=0,
        max=duration,
        on_change=seek_sldr_change,
        col=8.5
    )


    current_position_text=ft.TextButton(
        text=current_position_text_value,
        col=2,
        on_click=invert_current_position_text,
    )

    volume_sldr=ft.Slider(
        min=0,
        max=1,
        on_change=volume_sldr_change,
        col=2
    )


    page.overlay.append(audio)

    page.add(
        ft.ResponsiveRow([
            playbtn,
            seek_sldr,
        ]),
        ft.ResponsiveRow([
            current_position_text,
            volume_sldr   
        ])
    )
    page.on_resize=lambda _:page.update()




if __name__=="__main__":
    ft.app(target=main, port=1234, view=ft.AppView.WEB_BROWSER)