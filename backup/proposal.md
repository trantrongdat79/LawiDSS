DSS - Nhóm 5 

1. Tên đề tài và mô tả bài toán 

Tên đề tài: Hệ thống Tư vấn Pháp lý và Khuyến nghị hướng xử lý Luật Lao động (Labor Law Decision Support System) dựa trên RAG đa nguồn. 

Mô tả bối cảnh: Người lao động và bộ phận nhân sự (HR) thường xuyên gặp vướng mắc về hợp đồng, tiền lương, sa thải, thai sản... Tuy nhiên, văn bản pháp luật thường khô khan, khó hiểu và khó tra cứu. Các chatbot LLM thông thường lại dễ mắc lỗi "ảo giác" (bịa luật) và không biết áp dụng vào thực tiễn. 

Người dùng mục tiêu: Người lao động, chuyên viên nhân sự (HR), hoặc chủ doanh nghiệp nhỏ. 

Cách hệ thống hỗ trợ ra quyết định: Khi người dùng trình bày một tình huống vướng mắc, hệ thống sẽ phân tích dữ liệu để (1) Xác định đúng quy định pháp luật đang có hiệu lực, (2) Tìm kiếm các vụ việc thực tế tương tự đã được giải quyết trên báo chí, và (3) Đưa ra khuyến nghị để người dùng quyết định bước đi tiếp theo (VD: thương lượng, khiếu nại lên Sở LĐ-TB&XH, hay khởi kiện). 

2. Input và Output của hệ thống 

Dữ liệu đầu vào (Input): Câu hỏi hoặc đoạn văn bản mô tả tình huống thực tế của người dùng bằng ngôn ngữ tự nhiên (Ví dụ: "Công ty nợ lương 2 tháng, ép tôi ký giấy nghỉ việc thì tôi có kiện được không?"). 

Kết quả đầu ra (Output): Một báo cáo tư vấn hỗ trợ ra quyết định gồm 2 phần: 

Căn cứ pháp lý: Trích dẫn chính xác Điều, Khoản, tên văn bản luật đang còn hiệu lực liên quan đến tình huống. 

Khuyến nghị & Kiểm chứng thực tiễn: Tóm tắt một case-study thực tế trên báo chí/internet chứng minh cho quy định đó (kèm URL), và gợi ý các bước giải quyết hợp lý. 

3. Nguồn dữ liệu dự kiến sử dụng 

Hệ thống sử dụng kết hợp 2 nguồn dữ liệu để đảm bảo tính chính xác (luật) và tính thực tiễn (case study): 

Nguồn 1: Dữ liệu Văn bản Pháp luật (Tĩnh) 

Nguồn lấy: Tập dữ liệu open-source th1nhng0/vietnamese-legal-documents (Crawl từ cơ sở dữ liệu quốc gia vbpl.vn). 

Dạng dữ liệu: Bảng dữ liệu chứa văn bản HTML (Raw text) và Metadata (JSON/Parquet). 

Số lượng dự kiến: Khoảng hơn 176000 văn bản luật. 

Vai trò: Làm cơ sở tri thức (Knowledge Base) để chatbot đối chiếu và truy xuất luật chuẩn xác. 

Nguồn 2: Dữ liệu Báo chí và Tình huống thực tế (Động) 

Nguồn lấy: API Tìm kiếm (DuckDuckGo/Google Search) truy vấn trực tiếp vào các trang báo chính thống (Tuổi Trẻ, VNExpress) hoặc diễn đàn tư vấn luật. 

Dạng dữ liệu: Text (Nội dung bài báo được scrape tự động) và URL. 

Số lượng dự kiến: Truy xuất realtime (1-3 bài báo/truy vấn). 

Vai trò: Kiểm chứng thực tiễn, cung cấp ví dụ và án lệ để tăng sức thuyết phục cho các khuyến nghị của hệ thống. 

4. Phân tích dữ liệu cơ bản (EDA) 

Dựa trên kết quả chạy tiền xử lý trên tập dữ liệu Nguồn 1, nhóm đã rút ra các đặc điểm dữ liệu sau: 

Quy mô và Phân bố: Tập dữ liệu có 483 văn bản thuộc lĩnh vực Lao động. Trong đó, Quyết định chiếm 34.0%, Thông tư 33.5% và Nghị định 8.5%. 

Đặc điểm nổi bật: Có sự chênh lệch cực lớn về độ dài văn bản. Trung bình một văn bản dài 2.352 từ, nhưng văn bản dài nhất lên tới 62.335 từ, và có những mẫu dữ liệu rỗng. 

Khó khăn và Kế hoạch xử lý (Data Challenges): 

Dữ liệu nhiễu (Hết hiệu lực): EDA cho thấy có tới 52.0% văn bản đã hết hiệu lực, chỉ có 42.4% còn hiệu lực. Kế hoạch là sử dụng kỹ thuật Hard-Filtering trên Metadata để loại bỏ các văn bản cũ trước khi đưa vào mô hình tìm kiếm. 

Dữ liệu quá dài: Vì độ lệch chuẩn về số từ lớn, nếu cắt text theo kích thước cố định (Fixed-size chunking) sẽ làm vỡ ngữ nghĩa pháp lý. Nhóm dự kiến áp dụng kỹ thuật bóc tách bằng BeautifulSoup để chia nhỏ dữ liệu theo cấu trúc thẻ HTML (Chương, Điều, Khoản). 

5. Kế hoạch xây dựng 2 giải pháp 

Nhóm đề xuất 2 hướng giải pháp (Pipelines) để giải quyết bài toán và so sánh hiệu năng: 

Giải pháp 1: Mô hình RAG Truyền thống (Chỉ dùng Nguồn 1) 

Ý tưởng: Sử dụng kiến trúc Retrieval-Augmented Generation cơ bản. 

Cách xử lý: User nhập câu hỏi --> Chuyển thành Vector --> Tìm kiếm độ tương đồng (Semantic Search) trong Cơ sở dữ liệu Luật Lao động --> LLM tổng hợp câu trả lời. 

Kết quả kỳ vọng: Trả lời đúng luật cơ bản, nhưng thiếu tính cập nhật thực tiễn, không có ví dụ minh họa và không giải quyết trọn vẹn việc "tư vấn phương án". 

Giải pháp 2: Mô hình Agentic RAG Kết hợp Đa nguồn (Dùng Nguồn 1 + Nguồn 2) 

Ý tưởng: Xây dựng AI Agent có khả năng tự động suy luận và sử dụng công cụ. 

Cách xử lý: Agent đầu tiên sẽ truy xuất luật từ Vector Database (Nguồn 1). Sau đó, Agent tự động sinh ra một truy vấn tìm kiếm (Search Query), gọi API để quét báo chí (Nguồn 2), đọc bài báo và cuối cùng tổng hợp cả luật lẫn thực tiễn để đưa ra lời khuyên. 

Kết quả kỳ vọng: Hệ thống cung cấp được lời khuyên toàn diện, có chứng cứ thực tế, hỗ trợ người dùng ra quyết định mạnh mẽ và tin cậy hơn. 

6. Tiêu chí so sánh các giải pháp 

Nhóm sẽ đánh giá hiệu quả của 2 giải pháp dựa trên các tiêu chí đặc thù của hệ hỗ trợ ra quyết định: 

Độ chính xác truy xuất (Hit Rate / MRR): Đánh giá xem hệ thống có trích xuất đúng Điều luật quy định hay không. 

Độ phù hợp của khuyến nghị (Answer Relevance & Faithfulness): Sử dụng framework RAGAS để đo lường mức độ câu trả lời bám sát luật, không bịa đặt thông tin. 

Khả năng giải thích (Interpretability): Giải pháp 2 có khả năng cung cấp URL nguồn để người dùng tự kiểm chứng, giúp quyết định được đưa ra minh bạch hơn giải pháp 1. 

Thời gian xử lý (Latency): Đánh giá mức độ trễ của Giải pháp 2 (phải gọi thêm Web Search API) so với tốc độ phản hồi của Giải pháp 1. 

Mức độ hữu ích (User Utility): Đánh giá thông qua việc câu trả lời có tính ứng dụng (có ví dụ thực tế) hay chỉ là lý thuyết suông. 