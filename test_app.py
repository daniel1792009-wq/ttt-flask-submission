import importlib.util
from pathlib import Path
import unittest


class ContractTests(unittest.TestCase):
    def setUp(self):
        path = Path(__file__).with_name('app.py')
        self.assertTrue(path.exists(), 'The submission needs app.py')
        spec = importlib.util.spec_from_file_location('submission_app', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.client = module.app.test_client()

    def post(self, board, **fields):
        return self.client.post('/api/move', json={'board': board, 'agent': 'random', **fields})

    def test_page_and_assets(self):
        self.assertEqual(self.client.get('/').status_code, 200)
        for file in ('style.css', 'game.js'):
            with self.client.get('/static/' + file) as response:
                self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get('/api/move').status_code, 405)

    def test_random_move_supports_both_starters(self):
        for board in ('.........', 'O........', 'X...O....'):
            with self.subTest(board=board):
                response = self.post(board)
                self.assertEqual(response.status_code, 200)
                data = response.get_json()
                self.assertEqual(set(data), {'board', 'agent_move', 'status', 'winning_line'})
                move = data['agent_move']
                self.assertEqual(board[move], '.')
                self.assertEqual(data['board'], board[:move] + 'X' + board[move+1:])
                self.assertEqual(data['status'], 'playing')
                self.assertIsNone(data['winning_line'])

    def test_finished_boards_return_exact_status_and_no_move(self):
        for board, status, line in [('OOOXX....', 'human_wins', [0,1,2]),
                                   ('XXXOO....', 'agent_wins', [0,1,2]),
                                   ('OXOOXXXOO', 'draw', None)]:
            with self.subTest(board=board):
                response = self.post(board)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.get_json(), {'board': board, 'agent_move': None,
                    'status': status, 'winning_line': line})

    def test_last_empty_square_can_produce_agent_win_or_draw(self):
        for board, status, line in [('XX.OOXOXO', 'agent_wins', [0,1,2]),
                                   ('XOXXOOOX.', 'draw', None)]:
            response = self.post(board)
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data['status'], status)
            self.assertEqual(data['winning_line'], line)
            self.assertIsInstance(data['agent_move'], int)

    def test_missing_fields_unknown_agent_and_malformed_data(self):
        for payload in ({}, {'board': 'O........'}, {'agent': 'random'},
                        {'board':'O........', 'agent':'qtable'},
                        {'board':'O........', 'agent':'Random'},
                        {'board':[], 'agent':'random'}, None, [], 7):
            import json
            response = self.client.post('/api/move', data=json.dumps(payload), content_type='application/json')
            self.assertEqual(response.status_code, 400, payload)
            self.assertIn('error', response.get_json())
        response = self.client.post('/api/move', data='{broken', content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())

    def test_illegal_boards_return_400(self):
        for board in ('', 'short', 'Q........', 'OO.......', 'XX.......',
                      'OOOXXX...', 'XXXOO.O.O', 'X........'):
            response = self.post(board)
            self.assertEqual(response.status_code, 400, board)
            self.assertIn('error', response.get_json())


if __name__ == '__main__':
    unittest.main()
