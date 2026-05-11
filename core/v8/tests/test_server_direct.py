import sys, os, traceback
sys.path.insert(0, r'd:\Trae CN\github\nwacs\nwacs\core\v8')
os.chdir(r'd:\Trae CN\github\nwacs\nwacs\core\v8')

try:
    from nwacs_server import (
        creative_engine, genre_manager,
        _get_or_create_session, _generate_fallback_plots
    )
    from nwacs_server import PlotRequest
    from genre_profile_manager import GenreType

    req = PlotRequest(genre='玄幻', style='热血爽文', tone='紧张刺激', length='中长篇', theme='逆境成长')
    print('Request created')

    sid = _get_or_create_session(None)
    print(f'Session: {sid}')

    genre_map = {gt.label: gt for gt in GenreType}
    genre_enum = genre_map.get(req.genre)
    if genre_enum:
        genre_manager.set_genre(genre_enum)
        ctx = genre_manager.get_full_generation_context(include_pleasure=True)
        print(f'Genre context: {len(ctx)} chars')

    plots = _generate_fallback_plots(req)
    print(f'Fallback plots: {len(plots)}')
    for p in plots:
        print(f'  - {p["name"]}')
    print('All OK')

except Exception:
    traceback.print_exc()
