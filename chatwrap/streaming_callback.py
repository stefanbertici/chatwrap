class StreamingCallback:
    def __init__(self):
        self.full_response = []
    
    def __call__(self, token: str):
        """Handle each token as it arrives"""
        self.full_response.append(token)
        # Print the token immediately (you can modify this behavior)
        print(token, end='', flush=True)
    
    def get_full_response(self) -> str:
        """Return the complete response"""
        return ''.join(self.full_response)