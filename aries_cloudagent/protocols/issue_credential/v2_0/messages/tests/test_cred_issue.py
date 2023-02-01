from asynctest import mock as async_mock, TestCase as AsyncTestCase
from copy import deepcopy

from ......messaging.decorators.attach_decorator import AttachDecorator
from ......messaging.models.base import BaseModelError

from .....didcomm_prefix import DIDCommPrefix

from ...message_types import ATTACHMENT_FORMAT, CRED_20_ISSUE

from .. import cred_issue as test_module
from ..cred_format import V20CredFormat
from ..cred_issue import V20CredIssue


class TestV20CredIssue(AsyncTestCase):
    """Credential issue tests"""

    INDY_CRED = {
        "schema_id": "LjgpST2rjsoxYegQDRm7EL:2:bc-reg:1.0",
        "cred_def_id": "LjgpST2rjsoxYegQDRm7EL:3:CL:18:tag",
        "rev_reg_id": "LjgpST2rjsoxYegQDRm7EL:4:LjgpST2rjsoxYegQDRm7EL:3:CL:18:tag:CL_ACCUM:1",
        "values": {
            "busId": {"raw": "11155555", "encoded": "11155555"},
            "legalName": {
                "raw": "Babka Galaxy",
                "encoded": "107723975795096474174315415205901102419879622561395089750910511985549475735747",
            },
            "id": {"raw": "5", "encoded": "5"},
            "orgTypeId": {"raw": "1", "encoded": "1"},
            "effectiveDate": {
                "raw": "2012-12-01",
                "encoded": "58785836675119218543950531421539993546216494060018521243314445986885543138388",
            },
            "jurisdictionId": {"raw": "1", "encoded": "1"},
            "endDate": {
                "raw": "",
                "encoded": "102987336249554097029535212322581322789799900648198034993379397001115665086549",
            },
        },
        "signature": {
            "p_credential": {
                "m_2": "60025883287089799626689274984362649922028954710702989273350424792094051625907",
                "a": "33574785085847496372223801384241174668280696192852342004649681358898319989377891201713237406189930904621943660579244780378356431325594072391319837474469436200535615918847408676250915598611100068705846552950672619639766733118699744590194148554187848404028169947572858712592004307286251531728499790515868404251079046925435202101170698552776314885035743276729493940581544827310348632105741785505818500141788882165796461479904049413245974826370118124656594309043126033311790481868941737635314924873471152593101941520014919522243774177999183508913726745154494726830096189641688720673911842149721875115446765101254783088102",
                "e": "259344723055062059907025491480697571938277889515152306249728583105665800713306759149981690559193987143012367913206299323899696942213235956742929940839890541204554505134958365542601",
                "v": "8609087712648327689510560843448768242969198387856549646434987127729892694214386082710530362693226591495343780017066542203667948482019255226968628218013767981247576292730389932608795727994162072985790185993138122475561426334951896920290599111436791225402577204027790420706987810169826735050717355066696030347321187354133263894735515127702270039945304850524250402144664403971571904353156572222923701680935669167750650688016372444804704998087365054978152701248950729399377780813365024757989269208934482967970445445223084620917624825052959697120057360426040239100930790635416973591134497181715131476498510569905885753432826750000829362210364061766697316138646771666357343198925355584209303847699218225254051213598531538421032318684976506329062116913654998320196203740062523483508588929287294193683755114531891923195772740958",
            },
            "r_credential": {
                "sigma": "1 00F38C50E192DAF9133130888DA4A3291754B1A7D09A7DCCDD408D4E13F57267 1 0C6C9D8510580A8C9D8F0E21F51FF76E8F1419C2C909BBB9761AD9E75E46517F 2 095E45DDF417D05FB10933FFC63D474548B7FFFF7888802F07FFFFFF7D07A8A8",
                "c": "12F8B7BD08471C27F6AF8EE06374D200FCEA61718FACA61FD8B90EEED7A11AD6",
                "vr_prime_prime": "103015BFD51C02121DF61993973F312D5972EFF3B3B1B80BC614D5A747510366",
                "witness_signature": {
                    "sigma_i": "1 165767F82FF8FD92237985441D2C758706A5EC1D21FBEF8611C6AC4E3CAD10DA 1 1FC786E5CD2D8B30F1C567579B4EC143C5951B7464F78B86A03419CB335EA81B 1 0B1A1356056BEDF9C61AE2D66FF0405E3B1D934DAC97099BDF6AC3ECCBFAF745 1 106B15BC294810EEDF8AD363A85CC8ECC8AA061538BB31BAE5252377D77E7FA3 2 095E45DDF417D05FB10933FFC63D474548B7FFFF7888802F07FFFFFF7D07A8A8 1 0000000000000000000000000000000000000000000000000000000000000000",
                    "u_i": "1 017A61B7C8B5B80EB245BE6788A28F926D8CBB9829E657D437640EF09ACD0C80 1 1AF4229C05C728AEAEEE6FC411B357B857E773BA79FF677373A6BE8F60C02C3A 1 10CB82C4913E2324C06164BF22A2BD38CEE528C797C55061C2D2486C3F6BF747 1 116CE544B1CB99556BFC0621C57C3D9F2B78D034946322EEA218DFDBDD940EA3 2 095E45DDF417D05FB10933FFC63D474548B7FFFF7888802F07FFFFFF7D07A8A8 1 0000000000000000000000000000000000000000000000000000000000000000",
                    "g_i": "1 0042BF46E9BAE9696F394FE7C26AFDE3C8963A2A0658D4C32737405F1576EB46 1 0194E97A9D92D46AAD61DAE06926D3361F531EB10D03C7520F3BD69D3E49311C 2 095E45DDF417D05FB10933FFC63D474548B7FFFF7888802F07FFFFFF7D07A8A8",
                },
                "g_i": "1 0042BF46E9BAE9696F394FE7C26AFDE3C8963A2A0658D4C32737405F1576EB46 1 0194E97A9D92D46AAD61DAE06926D3361F531EB10D03C7520F3BD69D3E49311C 2 095E45DDF417D05FB10933FFC63D474548B7FFFF7888802F07FFFFFF7D07A8A8",
                "i": 1,
                "m2": "84B5722AE3A1CF27CB1EA56CD33D289CB87A4401C6B103D0D7B7EA869DAF6BB3",
            },
        },
        "signature_correctness_proof": {
            "se": "19792617148120152105226254239016588540058878757479987545108556827210662529343348161518678852958020771878595740749192412985440625444455760950622452787061547854765389520937092533324699495837410270589105368479415954380927050080439536019149709356488657394895381670676082762285043378943096265107585990717517541825549361747506315768406364562926877132553754434293723146759285511815164904802662712140021121638529229138315163496513377824821704164701067409581646133944445999621553849950380606679724798867481070896073389886302519310697801643262282687875393404841657943289557895895565050618203027512724917946512514235898009424924",
            "c": "20346348618412341786428948997994890734628812067145521907471418530511751955386",
        },
        "rev_reg": {
            "accum": "21 12E821764448DE2B5754DEC16864096CFAE4BB68D4DC0CE3E5C4849FC7CBCCC0C 21 11677132B2DFB0C291D0616811BF2AC0CD464A35FF6927B821A5EACF24D94F3A5 6 5471991A0950DBD431A4DD86A8AD101E033AB5EBC29A97CAFE0E4F2C426F5821 4 1B34A4C75174974A698061A09AFFED62B78AC2AAF876BF7788BAF3FC9A8B47DF 6 7D7C5E96AE17DDB21EC98378E3185707A69CF86426F5526C9A55D1FAA2F6FA83 4 277100094333E24170CD3B020B0C91A7E9510F69218AD96AC966565AEF66BC71"
        },
        "witness": {
            "omega": "21 136960A5E73C494F007BFE156889137E8B6DF301D5FF673C410CEE0F14AFAF1AE 21 132D4BA49C6BD8AB3CF52929D115976ABB1785D288F311CBB4455A85D07E2568C 6 70E7C40BA4F607262697556BB17FA6C85E9C188FA990264F4F031C39B5811239 4 351B98620B239DF14F3AB0B754C70597035A3B099D287A9855D11C55BA9F0C16 6 8AA1C473D792DF4F8287D0A93749046385CE411AAA1D685AA3C874C15B8628DB 4 0D6491BF5F127C1A0048CF137AEE17B62F4E49F3BDD9ECEBD14D56C43D211544"
        },
    }

    CRED_ISSUE = V20CredIssue(
        replacement_id="0",
        comment="Test",
        formats=[
            V20CredFormat(
                attach_id="indy",
                format_=ATTACHMENT_FORMAT[CRED_20_ISSUE][V20CredFormat.Format.INDY.api],
            )
        ],
        credentials_attach=[
            AttachDecorator.data_base64(
                mapping=INDY_CRED,
                ident="indy",
            )
        ],
    )

    CRED_ISSUE_MULTIPLE = V20CredIssue(
        replacement_id="0",
        comment="Test",
        formats=[
            V20CredFormat(
                attach_id="indy-0",
                format_=ATTACHMENT_FORMAT[CRED_20_ISSUE][V20CredFormat.Format.INDY.api],
            ),
            V20CredFormat(
                attach_id="indy-1",
                format_=ATTACHMENT_FORMAT[CRED_20_ISSUE][V20CredFormat.Format.INDY.api],
            ),
        ],
        credentials_attach=[
            AttachDecorator.data_base64(
                mapping=INDY_CRED,
                ident="indy-0",
            ),
            AttachDecorator.data_base64(
                mapping=INDY_CRED,
                ident="indy-1",
            ),
        ],
    )

    async def test_init_type(self):
        """Test initializer and type."""
        assert (
            TestV20CredIssue.CRED_ISSUE.credentials_attach[0].content
            == TestV20CredIssue.INDY_CRED
        )
        assert TestV20CredIssue.CRED_ISSUE.credentials_attach[  # auto-generates UUID4
            0
        ].ident
        assert TestV20CredIssue.CRED_ISSUE.attachment() == TestV20CredIssue.INDY_CRED
        assert TestV20CredIssue.CRED_ISSUE._type == DIDCommPrefix.qualify_current(
            CRED_20_ISSUE
        )
        assert (
            TestV20CredIssue.CRED_ISSUE_MULTIPLE.attachment_by_id("indy-1")
            == TestV20CredIssue.INDY_CRED
        )
        cred_issue_single = deepcopy(TestV20CredIssue.CRED_ISSUE)
        cred_issue_single.add_attachments(
            V20CredFormat(
                attach_id="indy-abc",
                format_=ATTACHMENT_FORMAT[CRED_20_ISSUE][V20CredFormat.Format.INDY.api],
            ),
            AttachDecorator.data_base64(
                mapping=TestV20CredIssue.INDY_CRED,
                ident="indy-abc",
            ),
        )
        assert (
            cred_issue_single.attachment_by_id("indy-abc") == TestV20CredIssue.INDY_CRED
        )

    async def test_attachment_no_target_format(self):
        """Test attachment behaviour for only unknown formats."""

        x_cred = V20CredIssue(
            comment="Test",
            formats=[V20CredFormat(attach_id="not_indy", format_="not_indy")],
            credentials_attach=[
                AttachDecorator.data_base64(
                    ident="not_indy", mapping=TestV20CredIssue.CRED_ISSUE.serialize()
                )
            ],
        )
        assert x_cred.attachment() is None

    async def test_deserialize(self):
        """Test deserialization."""
        obj = TestV20CredIssue.CRED_ISSUE.serialize()

        cred_issue = V20CredIssue.deserialize(obj)
        assert type(cred_issue) == V20CredIssue

        obj["credentials~attach"][0]["data"]["base64"] = "eyJub3QiOiAiaW5keSJ9"
        with self.assertRaises(BaseModelError):
            V20CredIssue.deserialize(obj)

        obj["credentials~attach"][0]["@id"] = "xxx"
        with self.assertRaises(BaseModelError):
            V20CredIssue.deserialize(obj)

        obj["credentials~attach"].append(  # more attachments than formats
            {
                "@id": "not_indy",
                "mime-type": "application/json",
                "data": {"base64": "eyJub3QiOiAiaW5keSJ9"},
            }
        )
        with self.assertRaises(BaseModelError):
            V20CredIssue.deserialize(obj)

        cred_issue.formats.append(  # unknown format: no validation
            V20CredFormat(
                attach_id="not_indy",
                format_="not_indy",
            )
        )
        obj = cred_issue.serialize()
        obj["credentials~attach"].append(
            {
                "@id": "not_indy",
                "mime-type": "application/json",
                "data": {"base64": "eyJub3QiOiAiaW5keSJ9"},
            }
        )
        V20CredIssue.deserialize(obj)

    async def test_serialize(self):
        """Test serialization."""
        obj = TestV20CredIssue.CRED_ISSUE

        with async_mock.patch.object(
            test_module.V20CredIssueSchema, "dump", async_mock.MagicMock()
        ) as mock_dump:
            cred_issue_dict = obj.serialize()
            mock_dump.assert_called_once_with(obj)

            assert cred_issue_dict is mock_dump.return_value

    async def test_make_model(self):
        """Test making model."""

        data = TestV20CredIssue.CRED_ISSUE.serialize()
        model_instance = V20CredIssue.deserialize(data)
        assert isinstance(model_instance, V20CredIssue)
